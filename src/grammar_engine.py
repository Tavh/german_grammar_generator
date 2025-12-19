"""
Grammar generation engine - pure functions for conjugation and sentence construction.
No I/O, no UI dependencies.
"""

from typing import Optional, List
from src.verb_model import Verb


# Präsens conjugation endings
PRÄSENS_ENDINGS = {
    "ich": "e",
    "du": "st",
    "er": "t",
    "sie": "t",
    "es": "t",
    "wir": "en",
    "ihr": "t",
    "Sie": "en",
    "sie_plural": "en"
}

# Irregular verb stems in Präsens (complete forms)
IRREGULAR_STEMS = {
    "sein": {"du": "bist", "er": "ist", "sie": "ist", "es": "ist"},
    "haben": {"du": "hast", "er": "hat", "sie": "hat", "es": "hat"},
    "werden": {"du": "wirst", "er": "wird", "sie": "wird", "es": "wird"},
    "wissen": {"du": "weißt", "er": "weiß", "sie": "weiß", "es": "weiß"},
    "mögen": {"du": "magst", "er": "mag", "sie": "mag", "es": "mag"},
    "können": {"du": "kannst", "er": "kann", "sie": "kann", "es": "kann"},
    "müssen": {"du": "musst", "er": "muss", "sie": "muss", "es": "muss"},
    "sollen": {"du": "sollst", "er": "soll", "sie": "soll", "es": "soll"},
    "wollen": {"du": "willst", "er": "will", "sie": "will", "es": "will"},
    "dürfen": {"du": "darfst", "er": "darf", "sie": "darf", "es": "darf"}
}

# Vowel changes for strong verbs in Präsens (e -> i for du/er/sie/es)
# Maps infinitive -> stem with vowel change for 2nd/3rd person singular
VOWEL_CHANGES = {
    "treffen": "triff",
    "helfen": "hilf",
    "nehmen": "nimm",
    "geben": "gib",
    "sehen": "sieh",
    "lesen": "lies",
    "essen": "iss",
    "sprechen": "sprich",
    "brechen": "brich"
}

# Reflexive pronouns
REFLEXIVE_PRONOUNS = {
    "ich": "mich",
    "du": "dich",
    "er": "sich",
    "sie": "sich",
    "es": "sich",
    "wir": "uns",
    "ihr": "euch",
    "Sie": "sich",
    "sie_plural": "sich"
}

# Case articles (definite)
ARTICLES_DAT = {
    "der": "dem",
    "die": "der",
    "das": "dem"
}

ARTICLES_AKK = {
    "der": "den",
    "die": "die",
    "das": "das"
}


def conjugate_präsens(verb: Verb, subject: str) -> str:
    """
    Conjugate a verb in Präsens for the given subject.
    
    MECHANICAL RULES (no inference):
    1. Check explicit irregular_present overrides first
    2. Check known irregular verbs (modal verbs, etc.)
    3. Apply known morphological rule: -ern/-eln verbs retain -er-
    4. Apply regular rule: stem + ending
    5. If form cannot be derived, raise error
    
    Args:
        verb: The verb to conjugate
        subject: Subject pronoun (ich, du, er, sie, es, wir, ihr, Sie, sie_plural)
    
    Returns:
        The conjugated verb form
    
    Raises:
        ValueError: If conjugated form cannot be derived from explicit data or known rules
    """
    infinitive = verb.infinitive
    
    # Rule 1: Check for explicit irregular Präsens overrides first
    if verb.irregular_present and subject in verb.irregular_present:
        return verb.irregular_present[subject]
    
    # Rule 2: Check for irregular verbs (complete forms) - modal verbs, etc.
    if infinitive in IRREGULAR_STEMS and subject in IRREGULAR_STEMS[infinitive]:
        return IRREGULAR_STEMS[infinitive][subject]
    
    # Rule 3: Known morphological rule: -ern/-eln verbs retain -er- before personal endings
    # Extract verb part (remove "sich " prefix if present)
    verb_part = infinitive
    if infinitive.startswith("sich "):
        verb_part = infinitive[5:]  # Remove "sich "
    
    if verb_part.endswith("ern") or verb_part.endswith("eln"):
        # Remove -n to get base, then add -er- before ending
        base_without_n = verb_part[:-1]  # e.g., "kümmern" -> "kümmer"
        ending = PRÄSENS_ENDINGS.get(subject)
        if ending is None:
            raise ValueError(f"Cannot conjugate '{infinitive}' for subject '{subject}': unknown subject")
        return base_without_n + ending
    
    # Rule 4: Regular conjugation: stem + ending
    # Special rule for du form: stems ending in s/ß/z/tz/x use "t" not "st"
    base_stem = verb.stem
    ending = PRÄSENS_ENDINGS.get(subject)
    
    if ending is None:
        raise ValueError(f"Cannot conjugate '{infinitive}' for subject '{subject}': unknown subject")
    
    if not base_stem:
        raise ValueError(f"Cannot conjugate '{infinitive}': stem is empty")
    
    # Special rule: du form with stems ending in s/ß/z/tz/x
    if subject == "du" and ending == "st":
        if base_stem and base_stem[-1] in ["s", "ß", "z", "x"]:
            return base_stem + "t"  # e.g., "putz" + "t" = "putzt", not "putzst"
        # Also check for "tz" ending (two characters)
        if base_stem and len(base_stem) >= 2 and base_stem[-2:] == "tz":
            return base_stem + "t"  # e.g., "schließ" + "t" = "schließt" (but "schließ" ends in ß, so first check handles it)
    
    return base_stem + ending


def get_reflexive_pronoun(verb: Verb, subject: str) -> Optional[str]:
    """Get the reflexive pronoun for a verb and subject."""
    if not verb.reflexive:
        return None
    return REFLEXIVE_PRONOUNS.get(subject)


def build_main_clause(
    subject: str,
    verb: Verb,
    verb_conjugated: str,
    objects: Optional[List[str]] = None,
    prepositional_phrases: Optional[List[str]] = None,
    time_expressions: Optional[List[str]] = None
) -> str:
    """
    Build a main clause (V2 word order) sentence.
    
    In main clauses, the verb is in position 2 (V2 rule).
    Structure: [Subject/Time/Other] [Verb] [Rest]
    
    Args:
        subject: Subject pronoun
        verb: Verb metadata
        verb_conjugated: Already conjugated verb form
        objects: List of objects (e.g., ["den Apfel"])
        prepositional_phrases: List of prepositional phrases (e.g., ["mit dem Freund"])
        time_expressions: List of time expressions (e.g., ["am Montag", "um Viertel nach fünf"])
    
    Returns:
        A complete sentence string
    """
    if objects is None:
        objects = []
    if prepositional_phrases is None:
        prepositional_phrases = []
    if time_expressions is None:
        time_expressions = []
    
    # Handle separable verbs
    if verb.separable and verb.prefix:
        # In main clauses, prefix goes to the end
        verb_without_prefix = verb_conjugated
        prefix = verb.prefix
    else:
        verb_without_prefix = verb_conjugated
        prefix = None
    
    # Get reflexive pronoun if needed
    reflexive_pronoun = get_reflexive_pronoun(verb, subject)
    
    # Position 1: Subject (or time expression if we want to emphasize time)
    # For simplicity, we'll use subject in position 1
    position_1 = subject.capitalize() if subject == subject.lower() else subject
    
    # Position 2: Conjugated verb (without prefix if separable)
    position_2 = verb_without_prefix
    
    # Rest of sentence: reflexive pronoun, objects, prepositional phrases, time expressions, prefix
    rest_parts = []
    
    # Reflexive pronoun comes early (after verb in position 2)
    if reflexive_pronoun:
        rest_parts.append(reflexive_pronoun)
    
    # Objects
    rest_parts.extend(objects)
    
    # Prepositional phrases
    rest_parts.extend(prepositional_phrases)
    
    # Time expressions
    rest_parts.extend(time_expressions)
    
    # Separable prefix goes at the end
    if prefix:
        rest_parts.append(prefix)
    
    # Combine
    sentence_parts = [position_1, position_2] + rest_parts
    return " ".join(sentence_parts)


def generate_sentence(
    subject: str,
    verb: Verb,
    objects: Optional[List[str]] = None,
    prepositional_phrases: Optional[List[str]] = None,
    time_expressions: Optional[List[str]] = None
) -> str:
    """
    Generate a complete sentence from components.
    
    MECHANICAL VALIDATION (no inference):
    - If valency is set, objects must be provided
    - If preposition is set, prepositional_phrases must be provided
    - If reflexive is true, reflexive pronoun is automatically added
    - If required_objects is set, all must be present
    - If impersonal is true, subject must be "es"
    
    Args:
        subject: Subject pronoun
        verb: Verb metadata
        objects: List of objects
        prepositional_phrases: List of prepositional phrases
        time_expressions: List of time expressions
    
    Returns:
        A complete German sentence
    
    Raises:
        ValueError: If required grammatical elements are missing
    """
    if objects is None:
        objects = []
    if prepositional_phrases is None:
        prepositional_phrases = []
    
    # MECHANICAL VALIDATION: Check all required elements are present
    
    # Rule 0: Frozen verbs cannot be freely generated
    # FROZEN VERB RULE: Verbs with experiencer datives, inverted semantics, or
    # impersonal subjects must not be freely generative. They require fixed_examples.
    # Examples: passieren, gehören, fehlen, gefallen, kosten
    if verb.generation_mode == "frozen":
        raise ValueError(
            f"Verb '{verb.infinitive}' is frozen and cannot be freely generated. "
            "Verbs with experiencer datives, inverted semantics, or impersonal "
            "subjects must use fixed_examples. Use fixed_examples instead."
        )
    
    # Rule 1: Impersonal verbs must use "es"
    if verb.impersonal and subject != "es":
        raise ValueError(f"Impersonal verb '{verb.infinitive}' requires subject 'es', got '{subject}'")
    
    # Rule 2: If valency is set, must have objects
    if verb.valency in ["dat", "akk"]:
        if not objects or len(objects) == 0:
            raise ValueError(f"Verb '{verb.infinitive}' has valency '{verb.valency}' but no objects provided")
    
    # Rule 3: If preposition is set, must have prepositional phrases
    if verb.preposition:
        if not prepositional_phrases or len(prepositional_phrases) == 0:
            raise ValueError(f"Verb '{verb.infinitive}' has preposition '{verb.preposition}' but no prepositional phrases provided")
    
    # Rule 4: If required_objects is set, must have all required cases
    if verb.required_objects:
        required_dat = "dat" in verb.required_objects
        required_akk = "akk" in verb.required_objects
        
        # Helper to detect case (same as in template_generator)
        dative_plural_nouns = ["Kindern", "Eltern", "Kollegen", "Freunden"]
        
        def is_dative(obj: str) -> bool:
            if obj.startswith(("dem ", "der ")):
                return True
            if obj.startswith("den "):
                noun = obj[4:]
                if noun in dative_plural_nouns:
                    return True
            return False
        
        def is_accusative(obj: str) -> bool:
            if obj.startswith(("die ", "das ", "einen ", "eine ", "ein ")):
                return True
            if obj.startswith("den "):
                noun = obj[4:]
                if noun not in dative_plural_nouns:
                    return True
            return False
        
        # Check all required objects are present
        has_dat = any(is_dative(obj) for obj in objects)
        has_akk = any(is_accusative(obj) for obj in objects)
        
        if required_dat and not has_dat:
            raise ValueError(f"Verb '{verb.infinitive}' requires dative object but none provided")
        if required_akk and not has_akk:
            raise ValueError(f"Verb '{verb.infinitive}' requires accusative object but none provided")
    
    # Rule 5: Reflexive verbs automatically get reflexive pronoun (handled in build_main_clause)
    # No validation needed - it's always added if verb.reflexive is True
    
    conjugated = conjugate_präsens(verb, subject)
    return build_main_clause(
        subject=subject,
        verb=verb,
        verb_conjugated=conjugated,
        objects=objects,
        prepositional_phrases=prepositional_phrases,
        time_expressions=time_expressions
    )

