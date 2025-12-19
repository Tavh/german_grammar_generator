# System Internal Correctness Audit
## A2.1 German Learning System

**Audit Scope**: Internal consistency of verb data relative to declared model rules.
**NOT auditing**: Linguistic completeness or real-world German usage.

---

## Audit Rules

A verb is **CORRECT** if:
- All generated sentences follow the verb's declared fields
- No sentence violates valency, reflexive, or preposition rules
- Objects come only from allowed lists

A verb is **NOT an error** if:
- It omits optional arguments
- It represents only one of several real-world usages
- It simplifies real German for pedagogy

**ONLY flag as errors**:
- Wrong conjugation forms
- Incorrect case usage relative to declared valency
- Reflexive usage missing or added incorrectly
- Prepositions used without being declared
- Objects used that are not in allowed lists

---

## Systematic Check Results

### 1. Verbs with valency but missing allowed_objects

Checking all verbs with `valency: "dat"` or `valency: "akk"`:

**❌ ERROR: "haben" (line 492-503)**
- **Field**: `valency: "akk"` but `allowed_objects` is missing
- **Issue**: System rule requires that if `valency` is set, `allowed_objects` must exist
- **Generated sentence would be**: Cannot generate (validation will fail)
- **System rule violation**: `valency: "akk"` → must have `allowed_objects` defined

**✅ VALID: "gefallen" (line 355-378)**
- Has `valency: "dat"` and `allowed_objects` with dative objects
- System rule satisfied

**❌ ERROR: "sprechen" (line 454-477)**
- **Field**: `valency: "dat"` but `allowed_objects` is missing
- **Issue**: System rule requires that if `valency` is set, `allowed_objects` must exist
- **Generated sentence would be**: Cannot generate (validation will fail)
- **System rule violation**: `valency: "dat"` → must have `allowed_objects` defined
- **Note**: Has `allowed_prepositional_objects` but valency requires `allowed_objects`

**❌ ERROR: "fragen" (line 556-572)**
- **Field**: `valency: "dat"` but `allowed_objects` is missing
- **Issue**: System rule requires that if `valency` is set, `allowed_objects` must exist
- **Generated sentence would be**: Cannot generate (validation will fail)
- **System rule violation**: `valency: "dat"` → must have `allowed_objects` defined
- **Note**: Has `allowed_prepositional_objects` but valency requires `allowed_objects`

---

### 2. Verbs with prepositions - all have allowed_prepositional_objects ✅

All verbs with `preposition` set also have `allowed_prepositional_objects` defined.

---

### 3. Verbs with required_objects

Checking ditransitive verbs with `required_objects: ["dat", "akk"]`:

**✅ VALID: "geben" (line 800-822)**
- Has `required_objects: ["dat", "akk"]`
- Has both dative and accusative objects in `allowed_objects`
- System rule satisfied

**✅ VALID: "bringen" (line 824-840)**
- Has `required_objects: ["dat", "akk"]`
- Has both dative and accusative objects in `allowed_objects`
- System rule satisfied

**✅ VALID: "schicken" (line 1142-1158)**
- Has `required_objects: ["dat", "akk"]`
- Has both dative and accusative objects in `allowed_objects`
- System rule satisfied

**✅ VALID: "zeigen" (line 1160-1176)**
- Has `required_objects: ["dat", "akk"]`
- Has both dative and accusative objects in `allowed_objects`
- System rule satisfied

**✅ VALID: "erklären" (line 1432-1448)**
- Has `required_objects: ["dat", "akk"]`
- Has both dative and accusative objects in `allowed_objects`
- System rule satisfied

**✅ VALID: "erzählen" (line 1474-1490)**
- Has `required_objects: ["dat", "akk"]`
- Has both dative and accusative objects in `allowed_objects`
- System rule satisfied

---

### 4. Reflexive verbs

**✅ VALID: "treffen" (line 3-26)**
- `reflexive: true` - correctly marked
- Has `allowed_prepositional_objects` for prepositional usage
- System rule satisfied

**✅ VALID: All other reflexive verbs**
- All correctly marked with `reflexive: true`
- System rule satisfied

---

### 5. Impersonal verbs

**✅ VALID: "passieren" (line 1552-1568)**
- `impersonal: true` - correctly marked
- System rule satisfied

---

### 6. Conjugation forms

Checking `irregular_present` fields for correctness:

**⚠️ AMBIGUOUS: Regular verbs with irregular_present field**

Several verbs have `irregular_present` fields but are actually regular:
- "arbeiten" (line 574-591): Regular verb, `irregular_present` field exists but forms are regular
- "mieten" (line 752-774): Regular verb, `irregular_present` field exists but forms are regular
- "beenden" (line 1408-1430): Regular verb, `irregular_present` field exists but forms are regular
- "antworten" (line 1450-1472): Regular verb, `irregular_present` field exists but forms are regular
- "sich verabreden" (line 1731-1753): Regular verb, `irregular_present` field exists but forms are regular
- "sich erkälten" (line 1914-1931): Regular verb, `irregular_present` field exists but forms are regular

**System impact**: These fields are harmless (conjugation will use them if present, but they're not needed). However, they're misleading. Since the system checks `irregular_present` first, these will work correctly, but the field is unnecessary.

**Verdict**: ⚠️ AMBIGUOUS - Not an error (system works correctly), but data is redundant.

---

### 7. Case consistency in allowed_objects

Checking if objects match declared valency:

**✅ VALID: All verbs with valency have objects with matching case**
- Dative verbs have dative objects (dem, der, den + plural)
- Accusative verbs have accusative objects (den, die, das, einen, eine, ein)
- System rule satisfied

---

## Summary

### ❌ ERRORS (Must Fix - System Rule Violations)

**Total: 3 verbs with valency but missing allowed_objects**

1. **"haben"** (line 492-503)
   - **Field**: `valency: "akk"` but `allowed_objects` is missing
   - **System rule violation**: Rule 1 in `template_generator.py`: "If valency is set, verb MUST have allowed_objects"
   - **Generated sentence would be**: `generate_exercise_instance()` returns `None` (validation fails)
   - **Fix required**: Either add `allowed_objects` or set `valency: null`

2. **"sprechen"** (line 454-477)
   - **Field**: `valency: "dat"` but `allowed_objects` is missing
   - **System rule violation**: Rule 1 in `template_generator.py`: "If valency is set, verb MUST have allowed_objects"
   - **Note**: Has `preposition: "mit"` and `allowed_prepositional_objects`, but system rule requires `allowed_objects` when `valency` is set
   - **Generated sentence would be**: `generate_exercise_instance()` returns `None` (validation fails)
   - **Fix required**: Either add `allowed_objects` with dative objects, or set `valency: null`

3. **"fragen"** (line 556-572)
   - **Field**: `valency: "dat"` but `allowed_objects` is missing
   - **System rule violation**: Rule 1 in `template_generator.py`: "If valency is set, verb MUST have allowed_objects"
   - **Note**: Has `preposition: "nach"` and `allowed_prepositional_objects`, but system rule requires `allowed_objects` when `valency` is set
   - **Generated sentence would be**: `generate_exercise_instance()` returns `None` (validation fails)
   - **Fix required**: Either add `allowed_objects` with dative objects, or set `valency: null`

### ⚠️ AMBIGUOUS (Not Errors - System Works Correctly)

**Regular verbs with unnecessary `irregular_present` fields (6 verbs)**
- "arbeiten", "mieten", "beenden", "antworten", "sich verabreden", "sich erkälten"
- **System impact**: None - conjugation works correctly (system checks `irregular_present` first, then falls back to regular)
- **Data quality**: Redundant but harmless
- **Verdict**: ✅ VALID - Not an error, system functions correctly

### ✅ VALID (All System Rules Satisfied)

- **Ditransitive verbs**: All 6 verbs with `required_objects: ["dat", "akk"]` have both cases in `allowed_objects`
- **Prepositional verbs**: All verbs with `preposition` set have `allowed_prepositional_objects`
- **Reflexive verbs**: All correctly marked with `reflexive: true`
- **Impersonal verbs**: "passieren" correctly marked with `impersonal: true`
- **Conjugation forms**: All `irregular_present` fields contain correct forms
- **Case consistency**: All objects match declared valency cases
- **All other verbs**: Follow system rules correctly

---

## Required Fixes

The 3 verbs with valency but missing allowed_objects will cause generation to fail (return None). They must either:
1. Have `allowed_objects` added, OR
2. Have `valency` set to `null` if objects are not required for this usage

**Note on "sprechen" and "fragen"**: These verbs have prepositions and the `valency` field appears to indicate the case of the prepositional object. However, the system rule requires `allowed_objects` when `valency` is set. The model design may need clarification: does `valency` refer to direct objects only, or can it refer to prepositional object case? Currently, the validation treats it as requiring direct objects.

