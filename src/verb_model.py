"""
Verb data model and loading logic.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict
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
            irregular_present=data.get("irregular_present")
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

