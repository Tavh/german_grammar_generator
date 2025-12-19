"""
Find verbs that should potentially be frozen based on semantic patterns.
"""
import sys
from pathlib import Path
import json

sys.stdout.reconfigure(encoding='utf-8')

# Load verbs
verbs_path = Path(__file__).parent / "data" / "verbs.json"
with open(verbs_path, "r", encoding="utf-8") as f:
    verbs = json.load(f)

print("=" * 80)
print("ANALYZING VERBS FOR FROZEN CANDIDATES")
print("=" * 80)

# Check current frozen verbs
frozen = [v for v in verbs if v.get("generation_mode") == "frozen"]
print(f"\nCurrent frozen verbs ({len(frozen)}):")
for v in frozen:
    has_examples = "fixed_examples" in v and v["fixed_examples"]
    print(f"  - {v['infinitive']}: {v.get('english_meaning', 'N/A')} {'✅' if has_examples else '❌ missing fixed_examples'}")

# Check for verbs with dative valency (potential experiencer datives)
print("\n" + "=" * 80)
print("DATIVE VERBS (checking for experiencer datives):")
print("=" * 80)

dative_verbs = [v for v in verbs if v.get("valency") == "dat" and v.get("generation_mode") != "frozen"]
for v in dative_verbs:
    print(f"  - {v['infinitive']}: {v.get('english_meaning', 'N/A')}")
    print(f"    Objects: {v.get('allowed_objects', [])[:3]}")

# Check for modal verbs
print("\n" + "=" * 80)
print("MODAL VERBS:")
print("=" * 80)

modal_verbs = [v for v in verbs if v.get("modal") == True]
for v in modal_verbs:
    is_frozen = v.get("generation_mode") == "frozen"
    print(f"  - {v['infinitive']}: {v.get('english_meaning', 'N/A')} {'(frozen)' if is_frozen else '(not frozen)'}")

# Check for verbs with inverted semantics patterns
print("\n" + "=" * 80)
print("VERBS WITH POTENTIALLY INVERTED SEMANTICS:")
print("=" * 80)

inverted_keywords = ["belong", "cost", "happen", "missing", "lack", "please", "like"]
for v in verbs:
    meaning = v.get("english_meaning", "").lower()
    if any(kw in meaning for kw in inverted_keywords):
        is_frozen = v.get("generation_mode") == "frozen"
        print(f"  - {v['infinitive']}: {v.get('english_meaning', 'N/A')} {'(frozen)' if is_frozen else '(not frozen)'}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total verbs: {len(verbs)}")
print(f"Frozen verbs: {len(frozen)}")
print(f"Dative verbs (not frozen): {len(dative_verbs)}")
print(f"Modal verbs: {len(modal_verbs)}")

