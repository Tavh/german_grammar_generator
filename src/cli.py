"""
CLI interface - thin wrapper around core logic.
"""

import random
from pathlib import Path
from src.verb_model import (
    load_verbs,
    filter_verbs_by_level,
    get_active_verbs,
    prioritize_active_verbs
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
    
    # Prioritize active verbs, but keep all available
    prioritized_verbs = prioritize_active_verbs(all_verbs, active_verb_infinitives, "A2")
    
    if not prioritized_verbs:
        print("Keine A2-Verben gefunden.")
        return
    
    # Filter verbs to only those with compatible templates
    verbs_with_templates = [
        verb for verb in prioritized_verbs 
        if find_compatible_template(verb, "A2") is not None
    ]
    
    if not verbs_with_templates:
        print("Keine Verben mit passenden Übungen gefunden.")
        return
    
    # Select verb: 70% chance from active verbs (if any), 30% from others
    active_with_templates = [v for v in verbs_with_templates if v.infinitive in active_verb_infinitives]
    others_with_templates = [v for v in verbs_with_templates if v.infinitive not in active_verb_infinitives]
    
    if active_with_templates and random.random() < 0.7:
        verb = random.choice(active_with_templates)
    elif others_with_templates:
        verb = random.choice(others_with_templates)
    else:
        verb = random.choice(verbs_with_templates)
    
    # Find compatible template (guaranteed to exist)
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

