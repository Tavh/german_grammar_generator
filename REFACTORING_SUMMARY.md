# Refactoring Summary: Usage-Centric Learning Model

## What Was Simplified

### Verb Database
- **Before**: 87 verbs with exhaustive A2.1 coverage
- **After**: 24 essential verbs covering key grammatical patterns
- **Rationale**: Focus on verbs learners actually use, not comprehensive coverage

### Template Patterns
- **Before**: 21 template patterns with many combinations
- **After**: 6 representative patterns covering essential structures
- **Rationale**: Avoid over-encoding; generate variations on demand

### Data Model
- **Before**: Single verb database
- **After**: Two-layer model:
  - Base verb library (shared, clean metadata)
  - Active verbs (personal, user-editable)

## What Was Added

### Active Verbs System
- `data/active_verbs.json` - User-editable list of verbs to practice
- Prioritization logic - 70% chance to select from active verbs
- All verbs remain available, but active ones are prioritized

### On-Demand Generation
- All verb forms generated from rules (already implemented)
- No pre-stored conjugated forms
- Templates generate exercises dynamically

## What Was Preserved

- Rule-based grammar engine (unchanged)
- UI-agnostic core logic (unchanged)
- Extensibility (data loading still abstracted)
- Template matching system (simplified but same approach)

## Key Changes

1. **Reduced verb count**: 87 → 24 essential verbs
2. **Reduced patterns**: 21 → 6 representative patterns
3. **Added active verbs**: Personal usage layer
4. **Prioritized selection**: Active verbs get 70% selection weight
5. **Simplified data**: Only essential metadata, no exhaustive combinations

## Files Changed

- `data/verbs.json` - Reduced to 24 verbs
- `data/template_patterns.json` - Reduced to 6 patterns
- `data/active_verbs.json` - **NEW** - User's active verb list
- `src/verb_model.py` - Added `load_active_verbs()` and `prioritize_active_verbs()`
- `src/cli.py` - Updated to use active verb prioritization
- `README.md` - Updated to reflect usage-centric model

## Result

**Less completeness, more usefulness.**

The system is now:
- Smaller and more focused
- User-customizable via active verbs
- Still extensible (add verbs/patterns as needed)
- More aligned with actual learning goals

