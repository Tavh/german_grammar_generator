"""
Verb data model and loading logic.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
import json
from pathlib import Path


@dataclass
class Verb:
    """Represents a German verb with its grammatical properties."""
    infinitive: str
    stem: str
    separable: bool
    prefix: str
    reflexive: bool
    preposition: Optional[str]
    valency: Optional[str]  # "akk", "dat", or None
    partizip_ii: Optional[str]
    auxiliary: str  # "haben" or "sein"
    levels: List[str]
    english_meaning: Optional[str] = None
    allowed_objects: Optional[List[str]] = None  # Verb-specific objects (Akk/Dat)
    allowed_prepositional_objects: Optional[List[str]] = None  # Verb-specific prepositional objects
    irregular_present: Optional[Dict[str, str]] = None  # Explicit Präsens overrides (e.g., {"du": "isst", "er": "isst"})
    required_objects: Optional[List[str]] = None  # Required object cases, e.g., ["dat", "akk"] for ditransitive verbs
    impersonal: bool = False  # True if verb is impersonal (requires es/neutral subject)

    @classmethod
    def from_dict(cls, data: dict) -> "Verb":
        """Create a Verb instance from a dictionary."""
        return cls(
            infinitive=data["infinitive"],
            stem=data["stem"],
            separable=data["separable"],
            prefix=data.get("prefix", ""),
            reflexive=data["reflexive"],
            preposition=data.get("preposition"),
            valency=data.get("valency"),
            partizip_ii=data.get("partizip_ii"),
            auxiliary=data["auxiliary"],
            levels=data["levels"],
            english_meaning=data.get("english_meaning"),
            allowed_objects=data.get("allowed_objects"),
            allowed_prepositional_objects=data.get("allowed_prepositional_objects"),
            irregular_present=data.get("irregular_present"),
            required_objects=data.get("required_objects"),
            impersonal=data.get("impersonal", False)
        )

    def to_dict(self) -> dict:
        """Convert Verb instance to dictionary."""
        return {
            "infinitive": self.infinitive,
            "stem": self.stem,
            "separable": self.separable,
            "prefix": self.prefix,
            "reflexive": self.reflexive,
            "preposition": self.preposition,
            "valency": self.valency,
            "partizip_ii": self.partizip_ii,
            "auxiliary": self.auxiliary,
            "levels": self.levels,
            "english_meaning": self.english_meaning
        }


def load_verbs(json_path: Path) -> List[Verb]:
    """Load verbs from a JSON file."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Verb.from_dict(item) for item in data]


def filter_verbs_by_level(verbs: List[Verb], level: str) -> List[Verb]:
    """Filter verbs by CEFR level."""
    return [v for v in verbs if level in v.levels]


def load_active_verbs(json_path: Path) -> List[str]:
    """Load active verb list from JSON file."""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("active_verbs", [])
    except FileNotFoundError:
        return []


def get_active_verbs(override: Optional[List[str]] = None) -> List[str]:
    """
    Get active verbs list.
    
    Args:
        override: Optional list to use instead of loading from file.
                  If None, loads from active_verbs.json
    
    Returns:
        List of active verb infinitives
    """
    if override is not None:
        return override
    
    # Default: load from file
    data_dir = Path(__file__).parent.parent / "data"
    active_verbs_path = data_dir / "active_verbs.json"
    return load_active_verbs(active_verbs_path)


def prioritize_active_verbs(
    verbs: List[Verb],
    active_verb_infinitives: List[str],
    level: str
) -> List[Verb]:
    """
    Prioritize active verbs while keeping all verbs available.
    Returns verbs with active verbs first, then others.
    """
    active = [v for v in verbs if v.infinitive in active_verb_infinitives and level in v.levels]
    others = [v for v in verbs if v.infinitive not in active_verb_infinitives and level in v.levels]
    return active + others


def select_verb_for_exercise(
    all_verbs: List[Verb],
    active_verb_infinitives: List[str],
    level: str,
    use_wider_pool: bool = True,
    active_weight: float = 0.75
) -> Optional[Verb]:
    """
    Select a verb for exercise generation.
    
    Core verb selection logic that is UI-agnostic.
    
    Args:
        all_verbs: Full base verb library (all available verbs)
        active_verb_infinitives: List of active verb infinitives (priority verbs)
        level: CEFR level (e.g., "A2")
        use_wider_pool: If True, allows selection from wider pool (non-active verbs).
                       If False, only selects from active verbs.
        active_weight: Probability of selecting from active verbs (0.0-1.0).
                      Default 0.75 (75% active, 25% wider pool).
    
    Returns:
        Selected Verb object, or None if no suitable verb found.
    """
    import random
    from src.exercise_templates import find_compatible_template
    
    # Filter to level
    level_verbs = [v for v in all_verbs if level in v.levels]
    
    if not level_verbs:
        return None
    
    # Filter to verbs with compatible templates
    verbs_with_templates = [
        verb for verb in level_verbs
        if find_compatible_template(verb, level) is not None
    ]
    
    if not verbs_with_templates:
        return None
    
    # Split into active and wider pool
    active_with_templates = [
        v for v in verbs_with_templates
        if v.infinitive in active_verb_infinitives
    ]
    
    wider_pool = [
        v for v in verbs_with_templates
        if v.infinitive not in active_verb_infinitives
    ]
    
    # Selection logic
    if not use_wider_pool:
        # Only from active verbs
        if active_with_templates:
            return random.choice(active_with_templates)
        else:
            # Fallback: no active verbs available, return None
            return None
    
    # Use weighted selection between active and wider pool
    if active_with_templates and random.random() < active_weight:
        # Select from active verbs
        return random.choice(active_with_templates)
    elif wider_pool:
        # Select from wider pool
        return random.choice(wider_pool)
    elif active_with_templates:
        # Fallback: only active verbs available
        return random.choice(active_with_templates)
    else:
        # No verbs available
        return None

