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
    
    Args:
        verb: The verb to conjugate
        subject: Subject pronoun (ich, du, er, sie, es, wir, ihr, Sie, sie_plural)
    
    Returns:
        The conjugated verb form
    """
    infinitive = verb.infinitive
    
    # Check for explicit irregular Präsens overrides first
    if verb.irregular_present and subject in verb.irregular_present:
        return verb.irregular_present[subject]
    
    # Check for irregular verbs (complete forms) - modal verbs, etc.
    if infinitive in IRREGULAR_STEMS and subject in IRREGULAR_STEMS[infinitive]:
        return IRREGULAR_STEMS[infinitive][subject]
    
    # Regular conjugation: stem + ending
    # No vowel-change inference - all irregular forms must be in irregular_present
    base_stem = verb.stem
    ending = PRÄSENS_ENDINGS.get(subject, "en")
    
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
    
    This is the main entry point for sentence generation.
    
    Args:
        subject: Subject pronoun
        verb: Verb metadata
        objects: List of objects
        prepositional_phrases: List of prepositional phrases
        time_expressions: List of time expressions
    
    Returns:
        A complete German sentence
    """
    conjugated = conjugate_präsens(verb, subject)
    return build_main_clause(
        subject=subject,
        verb=verb,
        verb_conjugated=conjugated,
        objects=objects,
        prepositional_phrases=prepositional_phrases,
        time_expressions=time_expressions
    )

