"""
CLI interface - thin wrapper around core logic.
"""

import random
from pathlib import Path
from src.verb_model import (
    load_verbs,
    filter_verbs_by_level,
    get_active_verbs,
    select_verb_for_exercise
)
from src.exercise_templates import find_compatible_template
from src.config import Config


def display_exercise(verb, exercise, config: Config):
    """
    Display the exercise to the user.
    
    Args:
        verb: The verb
        exercise: The exercise instance
        config: Configuration object (determines what to display)
    """
    print("\n" + "=" * 60)
    print(f"Verb: {verb.infinitive}")
    # Display meaning only if config allows it
    if config.show_meaning and verb.english_meaning:
        print(f"Meaning: {verb.english_meaning}")
    print("\nHinweise:")
    for hint in exercise.hints:
        print(f"  - {hint}")
    if exercise.description:
        print(f"\n{exercise.description}")
    print("=" * 60)
    print("\nDrücke ENTER, um die Lösung zu sehen...")


def display_solution(exercise):
    """Display the solution."""
    solution = exercise.generate_solution()
    print(f"\nLösung:\n{solution}\n")


def run_cli():
    """Main CLI entry point."""
    data_dir = Path(__file__).parent.parent / "data"
    
    # Load configuration
    from src.config import load_config
    config = load_config()
    
    # Load base verb library
    verbs_path = data_dir / "verbs.json"
    all_verbs = load_verbs(verbs_path)
    
    # Get active verbs (default: from active_verbs.json)
    active_verb_infinitives = get_active_verbs()
    
    # Use core selection function (CLI allows wider pool, same as before)
    verb = select_verb_for_exercise(
        all_verbs=all_verbs,
        active_verb_infinitives=active_verb_infinitives,
        level="A2",
        use_wider_pool=True,  # CLI always allows wider pool
        active_weight=0.7  # 70% active, 30% wider pool (maintains existing behavior)
    )
    
    if not verb:
        print("Keine passende Übung gefunden.")
        return
    
    # Find compatible template (guaranteed to exist from selection logic)
    exercise = find_compatible_template(verb, "A2")
    
    if not exercise:
        print(f"Keine passende Übung für '{verb.infinitive}' gefunden.")
        return
    
    # Display exercise (config determines what is shown)
    display_exercise(verb, exercise, config)
    
    # Wait for ENTER
    input()
    
    # Display solution
    display_solution(exercise)


if __name__ == "__main__":
    run_cli()

