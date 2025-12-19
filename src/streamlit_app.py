"""
Streamlit UI for German Grammar Generator.
Thin UI layer - all core logic remains UI-agnostic.
"""

import streamlit as st
import random
import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.verb_model import load_verbs, filter_verbs_by_level, get_active_verbs, prioritize_active_verbs
from src.exercise_templates import find_compatible_template
from src.config import Config, load_config


def initialize_session_state():
    """Initialize Streamlit session state."""
    if "exercise" not in st.session_state:
        st.session_state.exercise = None
    if "verb" not in st.session_state:
        st.session_state.verb = None
    if "solution_shown" not in st.session_state:
        st.session_state.solution_shown = False


def generate_new_exercise(all_verbs, active_verb_infinitives, level="A2"):
    """
    Generate a new exercise from active verbs.
    
    Args:
        all_verbs: All available verbs
        active_verb_infinitives: List of active verb infinitives
        level: CEFR level
    
    Returns:
        Tuple of (verb, exercise) or (None, None) if no exercise found
    """
    # Prioritize active verbs, but keep all available
    prioritized_verbs = prioritize_active_verbs(all_verbs, active_verb_infinitives, level)
    
    if not prioritized_verbs:
        return None, None
    
    # Filter verbs to only those with compatible templates
    verbs_with_templates = [
        verb for verb in prioritized_verbs 
        if find_compatible_template(verb, level) is not None
    ]
    
    if not verbs_with_templates:
        return None, None
    
    # Select verb: 70% chance from active verbs (if any), 30% from others
    active_with_templates = [v for v in verbs_with_templates if v.infinitive in active_verb_infinitives]
    others_with_templates = [v for v in verbs_with_templates if v.infinitive not in active_verb_infinitives]
    
    if active_with_templates and random.random() < 0.7:
        verb = random.choice(active_with_templates)
    elif others_with_templates:
        verb = random.choice(others_with_templates)
    else:
        verb = random.choice(verbs_with_templates)
    
    # Find compatible template
    exercise = find_compatible_template(verb, level)
    
    return verb, exercise


def main():
    """Main Streamlit app."""
    st.set_page_config(page_title="German Grammar Generator", page_icon="🇩🇪")
    
    initialize_session_state()
    
    # Load data
    data_dir = Path(__file__).parent.parent / "data"
    verbs_path = data_dir / "verbs.json"
    all_verbs = load_verbs(verbs_path)
    a2_verbs = filter_verbs_by_level(all_verbs, "A2")
    
    # Load default active verbs
    default_active = get_active_verbs()
    
    # Load config
    config = load_config()
    
    # Sidebar: Configuration
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Show meaning checkbox
        show_meaning = st.checkbox(
            "Show English meaning",
            value=config.show_meaning,
            help="Display English translations for verbs"
        )
        
        # Update config
        config.show_meaning = show_meaning
        
        st.divider()
        
        # Active verb selection
        st.header("📚 Active Verbs")
        st.caption("Select verbs to practice. Exercises prioritize selected verbs.")
        
        # Get all verb infinitives for multiselect
        all_verb_infinitives = [v.infinitive for v in a2_verbs]
        
        # Filter default_active to only include verbs that exist in database
        valid_default_active = [v for v in default_active if v in all_verb_infinitives]
        
        # Multiselect with default from active_verbs.json (filtered to valid verbs)
        selected_verbs = st.multiselect(
            "Choose active verbs",
            options=all_verb_infinitives,
            default=valid_default_active if valid_default_active else [],
            help="Select verbs you want to practice. Default selection comes from active_verbs.json"
        )
    
    # Main content
    st.title("🇩🇪 German Grammar Generator")
    st.caption("Practice German verb grammar through active sentence production")
    
    # Generate new exercise button
    if st.button("🎲 Next Exercise", type="primary", use_container_width=True):
        verb, exercise = generate_new_exercise(a2_verbs, selected_verbs)
        
        if verb and exercise:
            st.session_state.verb = verb
            st.session_state.exercise = exercise
            st.session_state.solution_shown = False
            st.rerun()
        else:
            st.error("Keine passende Übung gefunden. Bitte wähle andere Verben.")
    
    # Display current exercise
    if st.session_state.verb and st.session_state.exercise:
        exercise = st.session_state.exercise
        verb = st.session_state.verb
        
        st.divider()
        
        # Exercise display
        st.subheader("📝 Exercise")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"**Verb:** `{verb.infinitive}`")
        
        # Show meaning if configured
        if config.show_meaning and verb.english_meaning:
            st.caption(f"*{verb.english_meaning}*")
        
        st.markdown("**Hinweise:**")
        for hint in exercise.hints:
            st.markdown(f"- {hint}")
        
        if exercise.description:
            st.caption(exercise.description)
        
        st.divider()
        
        # Solution button
        if not st.session_state.solution_shown:
            if st.button("💡 Show Solution", use_container_width=True):
                st.session_state.solution_shown = True
                st.rerun()
        else:
            solution = exercise.generate_solution()
            st.success(f"**Lösung:** {solution}")
            
            if st.button("🔄 New Exercise", use_container_width=True):
                verb, exercise = generate_new_exercise(a2_verbs, selected_verbs)
                if verb and exercise:
                    st.session_state.verb = verb
                    st.session_state.exercise = exercise
                    st.session_state.solution_shown = False
                    st.rerun()
    
    else:
        # Initial state
        st.info("👆 Click 'Next Exercise' to start practicing!")
        st.caption(f"📊 {len(a2_verbs)} A2 verbs available | {len(selected_verbs)} active verbs selected")


if __name__ == "__main__":
    main()

