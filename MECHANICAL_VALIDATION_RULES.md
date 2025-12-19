# Mechanical Validation Rules

## Core Principle
**The verb JSON is the single source of truth. No inference, no guessing, no defaults.**

## Validation Rules

### 1. Valency Requires Objects
- **Rule**: If `valency` is `"dat"` or `"akk"`, the verb MUST have `allowed_objects` with matching case
- **Validation**: Check at template generation time
- **Failure**: Return `None` if `allowed_objects` is missing or empty
- **Example**: `helfen` has `valency: "dat"` → must have dative objects in `allowed_objects`

### 2. Preposition Requires Prepositional Objects
- **Rule**: If `preposition` is set, the verb MUST have `allowed_prepositional_objects`
- **Validation**: Check at template generation time
- **Failure**: Return `None` if `allowed_prepositional_objects` is missing or empty
- **Example**: `warten` has `preposition: "auf"` → must have objects in `allowed_prepositional_objects`

### 3. Required Objects Must All Be Present
- **Rule**: If `required_objects` is set (e.g., `["dat", "akk"]`), ALL must be satisfiable from `allowed_objects`
- **Validation**: Check at template generation and sentence generation time
- **Failure**: Return `None` at template generation, raise `ValueError` at sentence generation
- **Example**: `geben` has `required_objects: ["dat", "akk"]` → must have both dative AND accusative objects

### 4. Reflexive Verbs
- **Rule**: If `reflexive: true`, reflexive pronoun is automatically added
- **Validation**: Automatic (no explicit check needed)
- **Failure**: N/A (always handled)

### 5. Impersonal Verbs
- **Rule**: If `impersonal: true`, subject MUST be `"es"`
- **Validation**: Check at template generation and sentence generation time
- **Failure**: Return `None` at template generation, raise `ValueError` at sentence generation
- **Example**: `passieren` has `impersonal: true` → subject must be `"es"`

### 6. Conjugation Rules
- **Rule 1**: Check `irregular_present` overrides first (explicit data)
- **Rule 2**: Check known irregular verbs (modal verbs, etc.)
- **Rule 3**: Apply known morphological rule: `-ern/-eln` verbs retain `-er-`
- **Rule 4**: Apply regular rule: `stem + ending`
- **Failure**: Raise `ValueError` if form cannot be derived

## Generation Flow

1. **Template Generation** (`generate_exercise_instance`):
   - Validate verb data completeness
   - Check all required elements are available
   - Return `None` if validation fails (do not generate)

2. **Sentence Generation** (`generate_sentence`):
   - Validate all required elements are present
   - Raise `ValueError` if validation fails (explicit error, no guessing)

## What We DO NOT Do

- ❌ Infer missing objects
- ❌ Guess case from context
- ❌ Assume verbs can be used without required objects
- ❌ Create default objects
- ❌ Generate sentences with incomplete data
- ❌ Apply grammar rules not explicitly defined

## What We DO

- ✅ Use only explicit data from verb JSON
- ✅ Apply known morphological rules (`-ern/-eln`)
- ✅ Apply regular conjugation rules (stem + ending)
- ✅ Validate all requirements before generation
- ✅ Fail explicitly when data is missing
- ✅ Return `None` or raise `ValueError` instead of guessing

