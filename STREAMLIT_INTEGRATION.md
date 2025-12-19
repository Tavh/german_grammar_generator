# Streamlit UI Integration

## Architecture Overview

The system now supports both CLI and Streamlit UI while maintaining UI-agnostic core logic.

## Active Verbs Design

### Two-Layer System

1. **Default active verbs** (shared)
   - Loaded from `data/active_verbs.json`
   - Used by CLI (unchanged behavior)
   - Fallback for Streamlit

2. **Custom active verbs** (user-specific, optional)
   - Streamlit session state
   - User selects via multiselect widget
   - Overrides default for that session

### Abstraction: `get_active_verbs()`

```python
def get_active_verbs(override: Optional[List[str]] = None) -> List[str]:
    """
    Get active verbs list.
    
    Args:
        override: Optional list to use instead of loading from file.
                  If None, loads from active_verbs.json
    
    Returns:
        List of active verb infinitives
    """
```

**Usage:**
- CLI: `get_active_verbs()` → loads from file (default)
- Streamlit: `get_active_verbs(selected_verbs)` → uses session selection
- Future server: `get_active_verbs(user_preferences)` → per-user override

## File Structure

```
german_grammar_generator/
├── data/
│   ├── verbs.json              # Base verb library
│   ├── template_patterns.json  # Exercise templates
│   ├── active_verbs.json       # Default active verbs (CLI uses this)
│   └── config.json             # Configuration
├── src/
│   ├── verb_model.py           # Core: get_active_verbs() abstraction
│   ├── grammar_engine.py       # Core: UI-agnostic
│   ├── template_generator.py   # Core: UI-agnostic
│   ├── exercise_templates.py   # Core: UI-agnostic
│   ├── config.py               # Config management
│   ├── cli.py                  # CLI: uses get_active_verbs() (no override)
│   └── streamlit_app.py        # Streamlit: uses get_active_verbs(override)
└── requirements.txt            # Streamlit dependency
```

## How Active Verbs Flow

### CLI Flow (Unchanged)
```python
# CLI loads default
active_verbs = get_active_verbs()  # Loads from active_verbs.json
prioritized = prioritize_active_verbs(all_verbs, active_verbs, "A2")
```

### Streamlit Flow
```python
# Streamlit allows override
selected = st.multiselect(...)  # User selection
active_verbs = get_active_verbs(override=selected)  # Uses override
prioritized = prioritize_active_verbs(all_verbs, active_verbs, "A2")
```

### Future Server Flow
```python
# Server could load per user
user_prefs = load_user_preferences(user_id)
active_verbs = get_active_verbs(override=user_prefs)
```

## Streamlit UI Features

- **Multiselect widget** - Choose active verbs (defaults from `active_verbs.json`)
- **Show meaning checkbox** - Toggle English translations
- **Next exercise button** - Generate new exercises
- **Show solution button** - Reveal answers
- **Session state** - Maintains exercise and verb selection

## Core Logic Status

✅ **Completely UI-agnostic**
- Grammar engine: unchanged
- Exercise generation: unchanged
- Verb model: only added `get_active_verbs()` helper
- No UI-specific logic in core modules

✅ **CLI unchanged**
- Same behavior as before
- Uses `get_active_verbs()` (no override)
- Loads from `active_verbs.json` as before

✅ **Streamlit is thin wrapper**
- Uses same core functions
- Only adds UI widgets and session state
- No logic duplication

## Validation

- CLI works exactly as before ✓
- Streamlit allows per-session verb selection ✓
- Core logic receives active verbs as input (doesn't load files) ✓
- Future server can override active verbs per user ✓

