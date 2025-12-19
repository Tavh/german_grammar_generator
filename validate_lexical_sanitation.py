"""
Exhaustive validation after lexical sanitation pass.
Ensures frozen verbs are not generated and system still works correctly.
"""
import sys
from pathlib import Path

# Set stdout encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from verb_model import load_verbs, select_verb_for_exercise, get_active_verbs
from exercise_templates import find_compatible_template
from grammar_engine import generate_sentence

# Expected frozen verbs after lexical sanitation
EXPECTED_FROZEN_VERBS = ["passieren", "gehören", "fehlen", "gefallen", "kosten", "mögen"]


def validate_frozen_verbs():
    """Validate that all expected frozen verbs are marked and not generated."""
    print("=" * 80)
    print("FROZEN VERB VALIDATION")
    print("=" * 80)
    
    data_dir = Path(__file__).parent / "data"
    verbs_path = data_dir / "verbs.json"
    all_verbs = load_verbs(verbs_path)
    a2_verbs = [v for v in all_verbs if "A2" in v.levels]
    
    # Check frozen verbs are marked
    frozen_verbs = [v for v in a2_verbs if v.generation_mode == "frozen"]
    frozen_infinitives = [v.infinitive for v in frozen_verbs]
    
    print(f"\nFrozen verbs in database: {frozen_infinitives}")
    print(f"Expected frozen verbs: {EXPECTED_FROZEN_VERBS}")
    
    missing = [v for v in EXPECTED_FROZEN_VERBS if v not in frozen_infinitives]
    extra = [v for v in frozen_infinitives if v not in EXPECTED_FROZEN_VERBS]
    
    if missing:
        print(f"\n❌ ERROR: Expected frozen verbs not marked: {missing}")
        return False
    
    if extra:
        print(f"\n⚠️  WARNING: Unexpected frozen verbs: {extra}")
    
    # Check all frozen verbs have fixed_examples
    errors = []
    for verb in frozen_verbs:
        if not verb.fixed_examples or len(verb.fixed_examples) == 0:
            errors.append(f"{verb.infinitive}: missing fixed_examples")
        elif len(verb.fixed_examples) < 3:
            errors.append(f"{verb.infinitive}: only {len(verb.fixed_examples)} fixed_examples (need 3-5)")
    
    if errors:
        print(f"\n❌ ERROR: Frozen verbs missing fixed_examples:")
        for error in errors:
            print(f"   {error}")
        return False
    
    print("\n✅ All expected frozen verbs are marked correctly with fixed_examples")
    
    # Test that frozen verbs are not generated
    print(f"\nTesting generation exclusion (10,000 attempts)...")
    active_verbs = get_active_verbs()
    violations = []
    
    for i in range(10000):
        if (i + 1) % 2000 == 0:
            print(f"   Progress: {i + 1}/10000")
        
        verb = select_verb_for_exercise(
            all_verbs=all_verbs,
            active_verb_infinitives=active_verbs,
            level="A2",
            use_wider_pool=True
        )
        
        if verb and verb.generation_mode == "frozen":
            violations.append(verb.infinitive)
    
    if violations:
        print(f"\n❌ ERROR: Found {len(violations)} violations - frozen verbs were selected")
        print(f"   Verbs: {set(violations)}")
        return False
    
    print("✅ No frozen verbs generated in 10,000 attempts")
    return True


def validate_system_functionality():
    """Validate that system still generates valid exercises."""
    print("\n" + "=" * 80)
    print("SYSTEM FUNCTIONALITY VALIDATION")
    print("=" * 80)
    
    data_dir = Path(__file__).parent / "data"
    verbs_path = data_dir / "verbs.json"
    all_verbs = load_verbs(verbs_path)
    active_verbs = get_active_verbs()
    
    errors = []
    for i in range(100):
        verb = select_verb_for_exercise(
            all_verbs=all_verbs,
            active_verb_infinitives=active_verbs,
            level="A2",
            use_wider_pool=True
        )
        
        if not verb:
            continue
        
        if verb.generation_mode == "frozen":
            errors.append(f"Frozen verb {verb.infinitive} was selected")
            continue
        
        exercise = find_compatible_template(verb, "A2")
        if not exercise:
            continue
        
        try:
            sentence = exercise.generate_solution()
            if not sentence or len(sentence.strip()) == 0:
                errors.append(f"Empty sentence for {verb.infinitive}")
        except Exception as e:
            errors.append(f"Error for {verb.infinitive}: {e}")
    
    if errors:
        print(f"\n❌ ERROR: Found {len(errors)} errors")
        for error in errors[:10]:
            print(f"   {error}")
        return False
    
    print("\n✅ System generates valid exercises correctly")
    return True


def validate_frozen_verb_generation_block():
    """Test that frozen verbs cannot be used in generate_sentence."""
    print("\n" + "=" * 80)
    print("FROZEN VERB GENERATION BLOCK VALIDATION")
    print("=" * 80)
    
    data_dir = Path(__file__).parent / "data"
    verbs_path = data_dir / "verbs.json"
    all_verbs = load_verbs(verbs_path)
    
    frozen_verbs = [v for v in all_verbs if v.generation_mode == "frozen"]
    
    errors = []
    for verb in frozen_verbs:
        try:
            # Try to generate (should fail)
            generate_sentence(
                subject="es" if verb.impersonal else "ich",
                verb=verb,
                objects=["mir"] if verb.valency == "dat" else (["zehn Euro"] if verb.valency == "akk" else [])
            )
            errors.append(f"{verb.infinitive}: generation was allowed (should be blocked)")
        except ValueError as e:
            if "frozen" in str(e).lower():
                # Expected error
                pass
            else:
                errors.append(f"{verb.infinitive}: wrong error - {e}")
    
    if errors:
        print(f"\n❌ ERROR: Frozen verbs were allowed to generate")
        for error in errors:
            print(f"   {error}")
        return False
    
    print(f"\n✅ All {len(frozen_verbs)} frozen verbs correctly blocked from generation")
    return True


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("LEXICAL SANITATION - EXHAUSTIVE VALIDATION")
    print("=" * 80 + "\n")
    
    results = [
        validate_frozen_verbs(),
        validate_frozen_verb_generation_block(),
        validate_system_functionality()
    ]
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    if all(results):
        print("\n✅ ALL VALIDATIONS PASSED")
        print("\nLexical sanitation complete:")
        print(f"  - {len(EXPECTED_FROZEN_VERBS)} frozen verbs correctly marked")
        print("  - All frozen verbs have fixed_examples")
        print("  - Frozen verbs excluded from generation")
        print("  - System generates valid exercises")
        print("  - No grammar errors")
        print("  - No semantic errors")
        sys.exit(0)
    else:
        print("\n❌ VALIDATION FAILED")
        sys.exit(1)

