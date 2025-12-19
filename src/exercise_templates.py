"""
Exercise template system - compatibility layer for dynamic templates.
This module provides backward-compatible functions that use the new dynamic system.
"""

from typing import Optional
from pathlib import Path
from src.verb_model import Verb
from src.template_generator import (
    load_template_patterns,
    generate_exercise_for_verb,
    ExerciseInstance
)

# Cache for template patterns
_patterns_cache: Optional[list] = None


def _get_patterns() -> list:
    """Get template patterns, loading from cache or file."""
    global _patterns_cache
    if _patterns_cache is None:
        data_path = Path(__file__).parent.parent / "data" / "template_patterns.json"
        _patterns_cache = load_template_patterns(data_path)
    return _patterns_cache


def find_compatible_template(verb: Verb, level: str) -> Optional[ExerciseInstance]:
    """
    Find and generate a compatible exercise for the given verb and level.
    
    This function uses the dynamic template system to generate exercises
    based on verb properties rather than hardcoded templates.
    
    Returns:
        An ExerciseInstance (compatible with old template interface) or None
    """
    patterns = _get_patterns()
    return generate_exercise_for_verb(verb, level, patterns)

