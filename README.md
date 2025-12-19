# German Grammar Generator - Phase 1

A rule-based tool for practicing German verb grammar through active sentence production.

## Design Principles

- **Deterministic, rule-based logic only** - No AI, no NLP
- **UI-agnostic core** - Grammar logic is independent of interface
- **Explicit and readable** - Easy to modify and extend
- **Usage-centric** - Practice verbs you actually use, not exhaustive coverage

## Structure

```
german_grammar_generator/
├── data/
│   ├── verbs.json              # Base verb library (shared metadata)
│   ├── template_patterns.json  # Exercise template patterns
│   ├── active_verbs.json       # Default active verb list (shared)
│   └── config.json             # Configuration (show_meaning, etc.)
├── src/
│   ├── __init__.py
│   ├── verb_model.py           # Verb data model and loading
│   ├── grammar_engine.py       # Core grammar logic (pure functions, generates on demand)
│   ├── template_generator.py   # Dynamic template generation system
│   ├── exercise_templates.py   # Compatibility layer (uses template_generator)
│   ├── config.py               # Configuration management
│   ├── cli.py                  # CLI interface (thin wrapper)
│   └── streamlit_app.py        # Streamlit UI (thin wrapper)
└── README.md
```

## Usage

### CLI Interface

Run the CLI:

```bash
python -m src.cli
```

The tool will:
1. Load active verbs from `data/active_verbs.json`
2. Prioritize active verbs (70% chance) while keeping others available
3. Select a compatible exercise template
4. Display the verb and exercise hints
5. Wait for ENTER
6. Display the correct solution sentence

### Streamlit UI

Run the Streamlit interface:

```bash
streamlit run src/streamlit_app.py
```

The Streamlit UI provides:
- **Interactive verb selection** - Choose which verbs to practice (defaults from `active_verbs.json`)
- **Show/hide English meanings** - Toggle via checkbox
- **Next exercise button** - Generate new exercises on demand
- **Show solution button** - Reveal answers when ready

Active verbs are configurable per session in Streamlit, while CLI uses the default `active_verbs.json` file.

## Customizing Your Active Verbs

Edit `data/active_verbs.json` to add or remove verbs you want to practice most:

```json
{
  "active_verbs": [
    "treffen",
    "anrufen",
    "kaufen",
    "gehen"
  ]
}
```

Active verbs are prioritized in exercise selection, but all verbs remain available.

## Phase 1 Features

- **Base verb library** - 24 essential verbs covering key grammatical patterns:
  - Regular verbs (kaufen, essen, trinken, lesen, schreiben, machen)
  - Separable verbs (anrufen, aufstehen, einkaufen, ankommen)
  - Reflexive verbs (sich treffen, sich freuen, sich erinnern)
  - Reflexive + separable (sich anziehen, sich vorstellen)
  - Prepositional verbs (warten auf, denken an, sprechen mit)
  - Dative verbs (helfen, gefallen)
  - Modal verbs (können, müssen, wollen)
  - Verbs with sein auxiliary (gehen, kommen, ankommen, aufstehen)

- **Active verb system** - Personal list of verbs you use most
- **On-demand generation** - All verb forms generated from rules, not stored
- **Präsens conjugation** - With vowel changes and irregular forms
- **Main clause (V2) sentence construction**
- **Separable verb handling** - Prefix placement
- **Reflexive pronoun placement**
- **6 representative template patterns** - Covers essential structures without over-encoding

## Data Model

### Base Verb Library (`verbs.json`)
Clean verb metadata only:
- Grammatical properties (reflexive, separable, preposition, valency)
- Conjugation stem
- Auxiliary verb
- CEFR level tags
- No pre-generated forms

### Active Verbs (`active_verbs.json`)
Your personal usage layer:
- Simple list of verb infinitives
- User-editable
- Prioritized in exercise selection

### Template Patterns (`template_patterns.json`)
Small representative set:
- Matches verbs by grammatical properties
- Generates exercises dynamically
- No exhaustive combinations

## Design Philosophy

**Less completeness, more usefulness.**

- Verbs are treated as grammar bundles, not enumerated forms
- Forms generated on demand from rules
- Focus on verbs you actually use
- Extensible without bloat

## Future Extensions

- Web UI (core logic is UI-agnostic)
- Database backend (data loading is abstracted)
- Additional tenses
- Nebensätze (subordinate clauses)
- User input validation
