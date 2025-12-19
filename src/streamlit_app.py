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
        default_active_verbs: Default favourite verbs from active_verbs.json
    """
    if "exercise" not in st.session_state:
        st.session_state.exercise = None
    if "verb" not in st.session_state:
        st.session_state.verb = None
    if "solution_shown" not in st.session_state:
        st.session_state.solution_shown = False
    if "active_verbs" not in st.session_state:
        # Initialize with default favourite verbs
        st.session_state.active_verbs = default_active_verbs.copy()
    if "use_wider_pool" not in st.session_state:
        # Default: allow wider pool
        st.session_state.use_wider_pool = True
    if "active_weight" not in st.session_state:
        # Default: 75% favourite verbs, 25% new verbs
        st.session_state.active_weight = 75
    if "is_new_verb" not in st.session_state:
        # Track if current verb is from wider pool
        st.session_state.is_new_verb = False
    if "show_assistance" not in st.session_state:
        # Default: show assistance (guidance and usage examples)
        st.session_state.show_assistance = True
    if "user_answer" not in st.session_state:
        # Store user's typed answer
        st.session_state.user_answer = ""


def generate_new_exercise(all_verbs, active_verb_infinitives, use_wider_pool: bool, level="A2", active_weight: int = 75):
    """
    Generate a new exercise using core selection logic.
    
    Args:
        all_verbs: Full base verb library (all available verbs)
        active_verb_infinitives: List of favourite verb infinitives
        use_wider_pool: Whether to allow selection from wider pool
        level: CEFR level
        active_weight: Percentage of selecting from favourite verbs (0-100)
    
    Returns:
        Tuple of (verb, exercise, is_new_verb) or (None, None, False) if no exercise found
    """
    # Convert percentage to decimal for select_verb_for_exercise
    active_weight_decimal = active_weight / 100.0
    
    # Use core selection function (UI-agnostic)
    verb = select_verb_for_exercise(
        all_verbs=all_verbs,
        active_verb_infinitives=active_verb_infinitives,
        level=level,
        use_wider_pool=use_wider_pool,
        active_weight=active_weight_decimal
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
    
    # Load default favourite verbs from active_verbs.json
    default_active = get_active_verbs()
    
    # Filter default_active to only include verbs that exist in database
    all_verb_infinitives = [v.infinitive for v in a2_verbs]
    valid_default_active = [v for v in default_active if v in all_verb_infinitives]
    
    # Initialize session state with default favourite verbs
    initialize_session_state(valid_default_active)
    
    # Load config
    config = load_config()
    
    # Sidebar: Configuration
    with st.sidebar:
        st.header("⚙️ Settings")
        
        show_meaning = st.checkbox(
            "Show English meaning",
            value=config.show_meaning
        )
        config.show_meaning = show_meaning
        
        show_assistance = st.checkbox(
            "Show assistance",
            value=st.session_state.show_assistance
        )
        st.session_state.show_assistance = show_assistance
        
        use_wider_pool = st.checkbox(
            "Include new verbs",
            value=st.session_state.use_wider_pool
        )
        st.session_state.use_wider_pool = use_wider_pool
        
        st.divider()
        
        st.header("📚 Favourite Verbs")
        st.caption("Select verbs you want to practice most.")
        selected_verbs = st.multiselect(
            "Select verbs",
            options=all_verb_infinitives,
            default=st.session_state.active_verbs
        )
        st.session_state.active_verbs = selected_verbs
        st.caption(f"{len(a2_verbs)} total | {len(selected_verbs)} favourite")
        
        if use_wider_pool:
            active_weight = st.slider(
                "Favourite verb frequency",
                min_value=0,
                max_value=100,
                value=st.session_state.active_weight,
                step=5,
                format="%d%%",
                help="Percentage of exercises using favourite verbs (rest use new verbs)"
            )
            st.session_state.active_weight = active_weight
            new_pct = 100 - active_weight
            st.caption(f"{active_weight}% favourite | {new_pct}% new")
    
    # Main content
    st.title("🇩🇪 German Grammar Generator")
    
    # Auto-generate exercise on first load or if no exercise exists
    if not st.session_state.verb or not st.session_state.exercise:
        verb, exercise, is_new = generate_new_exercise(
            all_verbs=a2_verbs,
            active_verb_infinitives=st.session_state.active_verbs,
            use_wider_pool=st.session_state.use_wider_pool,
            level="A2",
            active_weight=st.session_state.active_weight
        )
        
        if verb and exercise:
            st.session_state.verb = verb
            st.session_state.exercise = exercise
            st.session_state.solution_shown = False
            st.session_state.user_answer = ""
            st.session_state.is_new_verb = is_new
            st.rerun()
        else:
            st.error("No exercise found. Select more verbs or enable 'Include new verbs'.")
            st.stop()
    
    # Display current exercise
    if st.session_state.verb and st.session_state.exercise:
        exercise = st.session_state.exercise
        verb = st.session_state.verb
        is_new_verb = st.session_state.is_new_verb
        
        st.divider()
        
        col1, col2 = st.columns([3, 1])
        with col1:
            verb_text = f"**Verb:** `{verb.infinitive}`"
            if is_new_verb:
                verb_text += " 🆕"
            st.markdown(verb_text)
        
        if is_new_verb and verb.infinitive not in st.session_state.active_verbs:
            with col2:
                if st.button("➕ Add to favourites", key="add_to_active"):
                    if verb.infinitive not in st.session_state.active_verbs:
                        st.session_state.active_verbs.append(verb.infinitive)
                    st.rerun()
        
        if config.show_meaning and verb.english_meaning:
            st.caption(f"*{verb.english_meaning}*")
        
        if st.session_state.show_assistance:
            for hint in exercise.hints:
                st.markdown(f"- {hint}")
        
        user_answer = st.text_input(
            "",
            value=st.session_state.user_answer,
            key="answer_input",
            placeholder="Type your sentence (practice only)",
            label_visibility="visible"
        )
        st.session_state.user_answer = user_answer
        
        if st.session_state.show_assistance:
            if not st.session_state.solution_shown:
                if st.button("💡 Show solution", use_container_width=True):
                    st.session_state.solution_shown = True
                    st.rerun()
            else:
                solution = exercise.generate_solution()
                st.success(solution)
        
        # New exercise button
        if st.button("🔄 New Exercise", use_container_width=True):
            verb, exercise, is_new = generate_new_exercise(
                all_verbs=a2_verbs,
                active_verb_infinitives=st.session_state.active_verbs,
                use_wider_pool=st.session_state.use_wider_pool,
                level="A2",
                active_weight=st.session_state.active_weight
            )
            if verb and exercise:
                st.session_state.verb = verb
                st.session_state.exercise = exercise
                st.session_state.solution_shown = False
                st.session_state.user_answer = ""
                st.session_state.is_new_verb = is_new
                st.rerun()


if __name__ == "__main__":
    main()

