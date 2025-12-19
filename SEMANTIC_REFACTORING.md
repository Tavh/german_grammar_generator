# Semantic Validity Refactoring

## Problem Solved

**Before**: Templates contained generic object examples that could combine with any verb, leading to semantically invalid sentences like "ich esse einen Kaffee".

**After**: Semantic content is constrained by verb metadata. Only verb-specific objects/prepositional objects are used.

## Changes Made

### 1. Simplified Templates (`data/template_patterns.json`)

**Before**: Templates contained concrete examples
```json
{
  "components": {
    "objects": [{
      "examples": ["einen Apfel", "das Buch", "einen Kaffee"]
    }]
  }
}
```

**After**: Templates describe only grammatical structure
```json
{
  "components": {
    "requires_object": true
  }
}
```

### 2. Extended Verb Metadata (`data/verbs.json`)

Added verb-specific semantic constraints:

```json
{
  "infinitive": "essen",
  "valency": "akk",
  "allowed_objects": [
    "einen Apfel",
    "eine Pizza",
    "das Brot",
    "einen Salat",
    "das Frühstück"
  ]
}
```

```json
{
  "infinitive": "warten",
  "preposition": "auf",
  "valency": "akk",
  "allowed_prepositional_objects": [
    "auf den Bus",
    "auf den Zug",
    "auf den Freund",
    "auf die Freundin"
  ]
}
```

### 3. Updated Verb Model (`src/verb_model.py`)

Added fields to `Verb` dataclass:
- `allowed_objects: Optional[List[str]]` - For Akkusativ/Dativ objects
- `allowed_prepositional_objects: Optional[List[str]]` - For prepositional objects

### 4. Refactored Generation Logic (`src/template_generator.py`)

**Key changes**:
- `generate_exercise_instance()` now returns `Optional[ExerciseInstance]`
- Returns `None` if verb lacks required fillers
- Uses ONLY `verb.allowed_objects` and `verb.allowed_prepositional_objects`
- Removed all generic example fallbacks
- `generate_exercise_for_verb()` tries multiple patterns until one with fillers is found

**Before**:
```python
# Used generic examples from template
obj = random.choice(obj_pattern["examples"])
```

**After**:
```python
# Uses only verb-specific fillers
if components.get("requires_object") and verb.allowed_objects:
    obj = random.choice(verb.allowed_objects)
else:
    return None  # Skip this template
```

## Result

✅ **Every generated sentence is semantically valid**
- "ich esse einen Apfel" ✓
- "ich trinke einen Kaffee" ✓
- "ich warte auf den Bus" ✓
- "ich esse einen Kaffee" ✗ (no longer possible)

✅ **Templates describe structure only**
✅ **Verbs define semantic content**
✅ **No fallback to generic examples**
✅ **Deterministic and rule-based**

## Example Output

```
essen        -> Du isst das Frühstück
  Objects: ['das Frühstück']

trinken      -> Du trinkst die Milch
  Objects: ['die Milch']

warten       -> Wir warten auf den Freund
  Prepositional: ['auf den Freund']

sprechen     -> Ich spreche mit der Freundin
  Prepositional: ['mit der Freundin']
```

All sentences are pedagogically correct A2-level German.

