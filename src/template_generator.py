"""
Dynamic template generation system.
Templates are patterns that match verbs based on their grammatical properties
and generate concrete exercises.
"""

import json
import random
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from src.verb_model import Verb
from src.grammar_engine import generate_sentence


@dataclass
class TemplatePattern:
    """Represents a template pattern that can match multiple verbs."""
    id: str
    level: str
    description: str
    requirements: Dict[str, Any]
    subjects: List[str]
    hint_patterns: Dict[str, Any]
    components: Dict[str, Any]
    
    @classmethod
    def from_dict(cls, data: dict) -> "TemplatePattern":
        """Create a TemplatePattern from a dictionary."""
        return cls(
            id=data["id"],
            level=data["level"],
            description=data["description"],
            requirements=data["requirements"],
            subjects=data["subjects"],
            hint_patterns=data["hint_patterns"],
            components=data["components"]
        )
    
    def matches_verb(self, verb: Verb) -> bool:
        """Check if this template pattern matches a verb's properties."""
        req = self.requirements
        
        # Check reflexive requirement
        if "reflexive" in req:
            if req["reflexive"] != verb.reflexive:
                return False
        
        # Check separable requirement
        if "separable" in req:
            if req["separable"] != verb.separable:
                return False
        
        # Check preposition requirement
        if "preposition" in req:
            has_prep = verb.preposition is not None
            if req["preposition"] != has_prep:
                return False
        
        # Check valency requirement
        if "valency" in req:
            if req["valency"] != verb.valency:
                return False
        
        return True


@dataclass
class ExerciseInstance:
    """A concrete exercise instance generated from a template pattern and verb."""
    template_id: str
    verb: Verb
    subject: str
    hints: List[str]
    objects: Optional[List[str]] = None
    prepositional_phrases: Optional[List[str]] = None
    time_expressions: Optional[List[str]] = None
    description: Optional[str] = None
    
    def generate_solution(self) -> str:
        """Generate the correct solution sentence."""
        return generate_sentence(
            subject=self.subject,
            verb=self.verb,
            objects=self.objects,
            prepositional_phrases=self.prepositional_phrases,
            time_expressions=self.time_expressions
        )


# Valency name mapping
VALENCY_NAMES = {
    "akk": "Akkusativ",
    "dat": "Dativ"
}


def load_template_patterns(json_path: Path) -> List[TemplatePattern]:
    """Load template patterns from JSON file."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [TemplatePattern.from_dict(item) for item in data]


def generate_exercise_instance(
    pattern: TemplatePattern,
    verb: Verb,
    subject: Optional[str] = None
) -> Optional[ExerciseInstance]:
    """
    Generate a concrete exercise instance from a template pattern and verb.
    Uses only verb-specific semantic fillers (allowed_objects, allowed_prepositional_objects).
    
    MECHANICAL RULES (no inference):
    - If valency is "dat" or "akk", verb MUST have allowed_objects with matching case
    - If preposition is set, verb MUST have allowed_prepositional_objects
    - If reflexive is true, reflexive pronoun is mandatory
    - If required_objects is set, all must be satisfiable from allowed_objects
    - If data is missing, return None (do not generate)
    
    Args:
        pattern: The template pattern
        verb: The verb to use
        subject: Optional specific subject, otherwise random from pattern's subjects
    
    Returns:
        A concrete ExerciseInstance, or None if verb lacks required fillers
    """
    # MECHANICAL VALIDATION: Check verb data completeness
    
    # Rule 1: If valency is set, verb MUST have allowed_objects
    if verb.valency in ["dat", "akk"]:
        if not verb.allowed_objects or len(verb.allowed_objects) == 0:
            return None  # Invalid: valency requires objects but none defined
    
    # Rule 2: If preposition is set, verb MUST have allowed_prepositional_objects
    if verb.preposition:
        if not verb.allowed_prepositional_objects or len(verb.allowed_prepositional_objects) == 0:
            return None  # Invalid: preposition requires objects but none defined
    
    # Rule 3: If reflexive is true, reflexive pronoun is mandatory (handled in sentence generation)
    # No validation needed here as it's automatically added
    
    # Rule 4: If required_objects is set, verify we can satisfy all requirements
    if verb.required_objects:
        if not verb.allowed_objects or len(verb.allowed_objects) == 0:
            return None  # Invalid: required_objects but no allowed_objects defined
    
    # Check if verb has required fillers for this template
    components = pattern.components
    
    # Check for required object (template requirement)
    if components.get("requires_object"):
        if not verb.allowed_objects or len(verb.allowed_objects) == 0:
            return None  # Verb doesn't have compatible objects
    
    # Check for required prepositional object (template requirement)
    if components.get("requires_prepositional_object"):
        if not verb.allowed_prepositional_objects or len(verb.allowed_prepositional_objects) == 0:
            return None  # Verb doesn't have compatible prepositional objects
    
    # Select subject
    if subject is None:
        subject = random.choice(pattern.subjects)
    
    # Enforce impersonal verb constraint: must use "es" or neutral subject
    if verb.impersonal:
        if subject not in ["es", "das", "etwas"]:
            return None  # Impersonal verb cannot use personal subject
        # If pattern doesn't allow "es", we can't use this verb
        if "es" not in pattern.subjects:
            return None
        subject = "es"  # Force "es" for impersonal verbs
    
    # Generate hints
    hints = []
    for hint_key, hint_value in pattern.hint_patterns.items():
        if hint_key == "subject":
            hints.append(subject)
        elif hint_key == "reflexive":
            if verb.reflexive:
                hints.append("sich")
        elif hint_key == "preposition":
            if verb.preposition:
                valency_name = VALENCY_NAMES.get(verb.valency, verb.valency or "")
                hints.append(f"{verb.preposition} ({valency_name})")
        elif hint_key == "object":
            # Will be filled from verb-specific objects
            pass
        elif hint_key == "prepositional_object":
            # Will be filled from verb-specific prepositional objects
            pass
    
    # Generate components using ONLY verb-specific fillers
    objects = []
    prepositional_phrases = []
    
    # MECHANICAL OBJECT GENERATION: Only use explicitly defined objects
    
    # Rule: If required_objects is set, must satisfy ALL requirements
    if verb.required_objects:
        required_dat = "dat" in verb.required_objects
        required_akk = "akk" in verb.required_objects
        
        # Helper to detect case from article (mechanical, no inference)
        # Dative plural nouns (explicit list from data)
        dative_plural_nouns = ["Kindern", "Eltern", "Kollegen", "Freunden"]
        
        def is_dative(obj: str) -> bool:
            if obj.startswith(("dem ", "der ")):
                return True
            # "den" + plural noun = dative plural (explicit check)
            if obj.startswith("den "):
                noun = obj[4:]  # Remove "den "
                if noun in dative_plural_nouns:
                    return True
            return False
        
        def is_accusative(obj: str) -> bool:
            if obj.startswith(("die ", "das ", "einen ", "eine ", "ein ")):
                return True
            # "den" + singular noun = accusative masculine (explicit check)
            if obj.startswith("den "):
                noun = obj[4:]  # Remove "den "
                if noun not in dative_plural_nouns:
                    return True  # Accusative if not known dative plural
            return False
        
        # For ditransitive verbs, we need both dative and accusative objects
        if required_dat:
            # Need a dative object - must exist in allowed_objects
            dat_objects = [obj for obj in verb.allowed_objects if is_dative(obj)]
            if not dat_objects:
                return None  # Cannot satisfy required dative object - data incomplete
            obj = random.choice(dat_objects)
            objects.append(obj)
            if "object" in pattern.hint_patterns:
                hints.append(obj)
        
        if required_akk:
            # Need an accusative object - must exist in allowed_objects
            akk_objects = [obj for obj in verb.allowed_objects if is_accusative(obj)]
            if not akk_objects:
                return None  # Cannot satisfy required accusative object - data incomplete
            obj = random.choice(akk_objects)
            objects.append(obj)
            if "object" in pattern.hint_patterns:
                hints.append(obj)
    
    # Rule: If valency is set (and not required_objects), must use object from allowed_objects
    elif verb.valency in ["dat", "akk"]:
        # valency requires an object - must be in allowed_objects
        if not verb.allowed_objects or len(verb.allowed_objects) == 0:
            return None  # Invalid: valency requires object but none defined
        obj = random.choice(verb.allowed_objects)
        objects.append(obj)
        if "object" in pattern.hint_patterns:
            hints.append(obj)
    
    # Rule: Template may also require an object (if not already satisfied by valency)
    elif components.get("requires_object"):
        if not verb.allowed_objects or len(verb.allowed_objects) == 0:
            return None  # Template requires object but verb has none
        obj = random.choice(verb.allowed_objects)
        objects.append(obj)
        if "object" in pattern.hint_patterns:
            hints.append(obj)
    
    # Rule: If preposition is set, MUST use object from allowed_prepositional_objects
    if verb.preposition:
        if not verb.allowed_prepositional_objects or len(verb.allowed_prepositional_objects) == 0:
            return None  # Invalid: preposition requires object but none defined
        prep_phrase = random.choice(verb.allowed_prepositional_objects)
        prepositional_phrases.append(prep_phrase)
        if "prepositional_object" in pattern.hint_patterns:
            hints.append(prep_phrase)
    
    # Rule: Template may also require prepositional object (if not already satisfied)
    elif components.get("requires_prepositional_object"):
        if not verb.allowed_prepositional_objects or len(verb.allowed_prepositional_objects) == 0:
            return None  # Template requires prepositional object but verb has none
        prep_phrase = random.choice(verb.allowed_prepositional_objects)
        prepositional_phrases.append(prep_phrase)
        if "prepositional_object" in pattern.hint_patterns:
            hints.append(prep_phrase)
    
    return ExerciseInstance(
        template_id=pattern.id,
        verb=verb,
        subject=subject,
        hints=hints,
        objects=objects if objects else None,
        prepositional_phrases=prepositional_phrases if prepositional_phrases else None,
        time_expressions=None,
        description=pattern.description
    )


def find_compatible_patterns(verb: Verb, level: str, patterns: List[TemplatePattern]) -> List[TemplatePattern]:
    """Find template patterns compatible with a verb and level."""
    compatible = []
    for pattern in patterns:
        if pattern.level == level and pattern.matches_verb(verb):
            compatible.append(pattern)
    return compatible


def generate_exercise_for_verb(
    verb: Verb,
    level: str,
    patterns: List[TemplatePattern],
    subject: Optional[str] = None
) -> Optional[ExerciseInstance]:
    """
    Generate an exercise instance for a verb.
    Only uses patterns where verb has required semantic fillers.
    
    Args:
        verb: The verb
        level: CEFR level
        patterns: List of available template patterns
        subject: Optional specific subject
    
    Returns:
        An ExerciseInstance or None if no compatible pattern with fillers found
    """
    compatible = find_compatible_patterns(verb, level, patterns)
    if not compatible:
        return None
    
    # Shuffle to randomize selection
    random.shuffle(compatible)
    
    # Try each compatible pattern until one works (has required fillers)
    for pattern in compatible:
        instance = generate_exercise_instance(pattern, verb, subject)
        if instance is not None:
            return instance
    
    # No pattern had required fillers
    return None

