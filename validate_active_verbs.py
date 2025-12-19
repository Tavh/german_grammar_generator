"""Validate active verbs list."""
import json
from pathlib import Path

# Load data
active_verbs_path = Path("data/active_verbs.json")
verbs_path = Path("data/verbs.json")

with open(active_verbs_path, "r", encoding="utf-8") as f:
    active_data = json.load(f)
    active_verbs = active_data["active_verbs"]

with open(verbs_path, "r", encoding="utf-8") as f:
    all_verbs = json.load(f)

# Create lookup
verb_lookup = {v["infinitive"]: v for v in all_verbs}

print("=" * 80)
print("ACTIVE VERBS VALIDATION")
print("=" * 80)
print(f"\nTotal verbs in list: {len(active_verbs)}")
print(f"Unique verbs: {len(set(active_verbs))}")

# Check for duplicates
duplicates = []
seen = set()
for v in active_verbs:
    if v in seen:
        duplicates.append(v)
    seen.add(v)

if duplicates:
    print(f"\n[ERROR] Duplicates found: {duplicates}")
else:
    print("\n[OK] No duplicates")

# Check if all exist
missing = [v for v in active_verbs if v not in verb_lookup]
if missing:
    print(f"\n[ERROR] Missing from database: {missing}")
else:
    print("\n[OK] All verbs exist in database")

# Check A2 level
not_a2 = []
frozen = []
for v in active_verbs:
    if v in verb_lookup:
        verb = verb_lookup[v]
        if "A2" not in verb.get("levels", []):
            not_a2.append(v)
        if verb.get("generation_mode") == "frozen":
            frozen.append(v)

if not_a2:
    print(f"\n[WARNING] Not A2 level: {not_a2}")
else:
    print("\n[OK] All verbs are A2 level")

if frozen:
    print(f"\n[WARNING] Frozen verbs (cannot be freely generated): {frozen}")

# Check for natural/common verbs
print("\n" + "=" * 80)
print("VERB LIST REVIEW")
print("=" * 80)

# Group by category
categories = {
    "Essential": ["sein", "haben"],
    "Movement": ["gehen", "kommen", "fahren", "bleiben", "aufstehen", "ankommen", "mitkommen"],
    "Communication": ["treffen", "sich treffen", "anrufen", "sprechen", "sagen", "fragen"],
    "Work/Study": ["arbeiten", "lernen", "machen", "versuchen", "brauchen"],
    "Shopping": ["kaufen", "bezahlen", "bestellen", "suchen", "finden"],
    "Food/Drink": ["essen", "trinken"],
    "Help/Wait": ["helfen", "warten"],
    "Living": ["wohnen", "leben", "mieten"],
    "Give/Take": ["nehmen", "geben", "bringen"],
    "Reflexive": ["sich erinnern", "sich freuen", "sich interessieren"],
    "Mental": ["denken"]
}

print("\nCurrent organization:")
for cat, verbs in categories.items():
    print(f"\n{cat}:")
    for v in verbs:
        if v in active_verbs:
            if v in verb_lookup and "A2" in verb_lookup[v].get("levels", []):
                status = "[OK]"
            else:
                status = "[ERROR]"
            print(f"  {status} {v}")

# Recommendations
print("\n" + "=" * 80)
print("RECOMMENDATIONS")
print("=" * 80)

issues = []
if duplicates:
    issues.append(f"Remove duplicates: {duplicates}")
if missing:
    issues.append(f"Remove missing verbs: {missing}")
if not_a2:
    issues.append(f"Remove non-A2 verbs: {not_a2}")
if frozen:
    issues.append(f"Remove frozen verbs (cannot be generated): {frozen}")

if issues:
    print("\nIssues to fix:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("\n[OK] No issues found!")

# Suggest natural, commonly used A2 verbs
print("\n" + "=" * 80)
print("SUGGESTED NATURAL A2 VERBS")
print("=" * 80)

suggested_essential = [
    "sein", "haben",  # Essential
    "gehen", "kommen", "fahren", "bleiben",  # Movement
    "machen", "kaufen", "essen", "trinken",  # Common actions
    "sehen", "hören", "sprechen", "sagen",  # Perception/communication
    "arbeiten", "lernen", "wohnen", "leben",  # Daily life
    "helfen", "geben", "nehmen", "bringen",  # Common interactions
    "anrufen", "aufstehen", "ankommen",  # Separable verbs
    "sich freuen", "sich treffen",  # Reflexive verbs
]

print("\nSuggested list (natural, commonly used):")
for v in suggested_essential:
    if v in verb_lookup:
        verb = verb_lookup[v]
        is_a2 = "A2" in verb.get("levels", [])
        is_frozen = verb.get("generation_mode") == "frozen"
        if is_a2 and not is_frozen:
            status = "[OK]"
        else:
            status = "[SKIP]"
        print(f"  {status} {v}")

