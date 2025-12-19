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

from src.verb_model import (
    load_verbs,
    filter_verbs_by_level,
    get_active_verbs,
    select_verb_for_exercise
)
from src.exercise_templates import find_compatible_template
from src.config import Config, load_config


def initialize_session_state(default_active_verbs: list):
    """
    Initialize Streamlit session state.
    
    Args:
        default_active_verbs: Default active verbs from active_verbs.json
    """
    if "exercise" not in st.session_state:
        st.session_state.exercise = None
    if "verb" not in st.session_state:
        st.session_state.verb = None
    if "solution_shown" not in st.session_state:
        st.session_state.solution_shown = False
    if "active_verbs" not in st.session_state:
        # Initialize with default active verbs
        st.session_state.active_verbs = default_active_verbs.copy()
    if "use_wider_pool" not in st.session_state:
        # Default: allow wider pool
        st.session_state.use_wider_pool = True
    if "is_new_verb" not in st.session_state:
        # Track if current verb is from wider pool
        st.session_state.is_new_verb = False


def generate_new_exercise(all_verbs, active_verb_infinitives, use_wider_pool: bool, level="A2"):
    """
    Generate a new exercise using core selection logic.
    
    Args:
        all_verbs: Full base verb library (all available verbs)
        active_verb_infinitives: List of active verb infinitives
        use_wider_pool: Whether to allow selection from wider pool
        level: CEFR level
    
    Returns:
        Tuple of (verb, exercise, is_new_verb) or (None, None, False) if no exercise found
    """
    # Use core selection function (UI-agnostic)
    verb = select_verb_for_exercise(
        all_verbs=all_verbs,
        active_verb_infinitives=active_verb_infinitives,
        level=level,
        use_wider_pool=use_wider_pool,
        active_weight=0.75  # 75% active, 25% wider pool
    )
    
    if not verb:
        return None, None, False
    
    # Check if verb is from wider pool (new verb)
    is_new_verb = verb.infinitive not in active_verb_infinitives
    
    # Find compatible template
    exercise = find_compatible_template(verb, level)
    
    if not exercise:
        return None, None, False
    
    return verb, exercise, is_new_verb


def main():
    """Main Streamlit app."""
    st.set_page_config(page_title="German Grammar Generator", page_icon="🇩🇪")
    
    # Load data
    data_dir = Path(__file__).parent.parent / "data"
    verbs_path = data_dir / "verbs.json"
    all_verbs = load_verbs(verbs_path)
    a2_verbs = filter_verbs_by_level(all_verbs, "A2")
    
    # Load default active verbs from active_verbs.json
    default_active = get_active_verbs()
    
    # Filter default_active to only include verbs that exist in database
    all_verb_infinitives = [v.infinitive for v in a2_verbs]
    valid_default_active = [v for v in default_active if v in all_verb_infinitives]
    
    # Initialize session state with default active verbs
    initialize_session_state(valid_default_active)
    
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
        
        # Wider pool toggle
        st.header("🔍 Verb Discovery")
        use_wider_pool = st.checkbox(
            "☐ Occasionally include new verbs",
            value=st.session_state.use_wider_pool,
            help="When enabled, exercises may include verbs from the wider pool (not just active verbs). "
                 "This allows you to discover new verbs while still prioritizing your active verbs."
        )
        st.session_state.use_wider_pool = use_wider_pool
        
        st.divider()
        
        # Active verb selection
        st.header("📚 Active Verbs")
        st.caption("Select verbs to practice. Exercises prioritize selected verbs (~75% of the time).")
        
        # Multiselect with current session state
        selected_verbs = st.multiselect(
            "Choose active verbs",
            options=all_verb_infinitives,
            default=st.session_state.active_verbs,
            help="Select verbs you want to practice. Default selection comes from active_verbs.json"
        )
        
        # Update session state
        st.session_state.active_verbs = selected_verbs
        
        # Stats
        st.caption(f"📊 {len(a2_verbs)} total A2 verbs | {len(selected_verbs)} active")
    
    # Main content
    st.title("🇩🇪 German Grammar Generator")
    st.caption("Practice German verb grammar through active sentence production")
    
    # Generate new exercise button
    if st.button("🎲 Next Exercise", type="primary", use_container_width=True):
        verb, exercise, is_new = generate_new_exercise(
            all_verbs=a2_verbs,
            active_verb_infinitives=st.session_state.active_verbs,
            use_wider_pool=st.session_state.use_wider_pool,
            level="A2"
        )
        
        if verb and exercise:
            st.session_state.verb = verb
            st.session_state.exercise = exercise
            st.session_state.solution_shown = False
            st.session_state.is_new_verb = is_new
            st.rerun()
        else:
            st.error("Keine passende Übung gefunden. Bitte wähle andere Verben oder aktiviere 'Occasionally include new verbs'.")
    
    # Display current exercise
    if st.session_state.verb and st.session_state.exercise:
        exercise = st.session_state.exercise
        verb = st.session_state.verb
        is_new_verb = st.session_state.is_new_verb
        
        st.divider()
        
        # Exercise display
        st.subheader("📝 Exercise")
        
        # Verb header with "new" indicator
        col1, col2 = st.columns([3, 1])
        with col1:
            verb_display = f"**Verb:** `{verb.infinitive}`"
            if is_new_verb:
                verb_display += " 🆕 *New verb*"
            st.markdown(verb_display)
        
        # Add to active button (if new verb)
        if is_new_verb and verb.infinitive not in st.session_state.active_verbs:
            with col2:
                if st.button("➕ Add to Active", key="add_to_active"):
                    if verb.infinitive not in st.session_state.active_verbs:
                        st.session_state.active_verbs.append(verb.infinitive)
                    st.success(f"Added `{verb.infinitive}` to active verbs!")
                    st.rerun()
        
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
                verb, exercise, is_new = generate_new_exercise(
                    all_verbs=a2_verbs,
                    active_verb_infinitives=st.session_state.active_verbs,
                    use_wider_pool=st.session_state.use_wider_pool,
                    level="A2"
                )
                if verb and exercise:
                    st.session_state.verb = verb
                    st.session_state.exercise = exercise
                    st.session_state.solution_shown = False
                    st.session_state.is_new_verb = is_new
                    st.rerun()
    
    else:
        # Initial state
        st.info("👆 Click 'Next Exercise' to start practicing!")
        st.caption(f"📊 {len(a2_verbs)} A2 verbs available | {len(st.session_state.active_verbs)} active verbs selected")


if __name__ == "__main__":
    main()

