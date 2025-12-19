"""
Test suite for Präsens conjugation correctness.

Tests are deterministic with explicit expected outputs.
No randomness, no UI/CLI dependencies.
"""

import json
import pytest
from pathlib import Path

from src.verb_model import Verb
from src.grammar_engine import conjugate_präsens


# Load verbs once for all tests
_VERBS_CACHE = None


def _load_verbs():
    """Load verbs from JSON file."""
    global _VERBS_CACHE
    if _VERBS_CACHE is None:
        data_dir = Path(__file__).parent.parent / "data"
        verbs_path = data_dir / "verbs.json"
        with open(verbs_path, "r", encoding="utf-8") as f:
            _VERBS_CACHE = json.load(f)
    return _VERBS_CACHE


def _get_verb(infinitive: str) -> Verb:
    """Get a Verb object by infinitive."""
    verbs = _load_verbs()
    verb_dict = [v for v in verbs if v["infinitive"] == infinitive][0]
    return Verb.from_dict(verb_dict)


# ============================================================================
# 1. Stem-change verbs
# ============================================================================

def test_essen_du():
    """Test essen: du isst"""
    verb = _get_verb("essen")
    result = conjugate_präsens(verb, "du")
    assert result == "isst"


def test_essen_er():
    """Test essen: er isst"""
    verb = _get_verb("essen")
    result = conjugate_präsens(verb, "er")
    assert result == "isst"


def test_lesen_du():
    """Test lesen: du liest"""
    verb = _get_verb("lesen")
    result = conjugate_präsens(verb, "du")
    assert result == "liest"


def test_lesen_sie():
    """Test lesen: sie liest"""
    verb = _get_verb("lesen")
    result = conjugate_präsens(verb, "sie")
    assert result == "liest"


def test_nehmen_du():
    """Test nehmen: du nimmst"""
    verb = _get_verb("nehmen")
    result = conjugate_präsens(verb, "du")
    assert result == "nimmst"


def test_nehmen_er():
    """Test nehmen: er nimmt"""
    verb = _get_verb("nehmen")
    result = conjugate_präsens(verb, "er")
    assert result == "nimmt"


def test_sprechen_du():
    """Test sprechen: du sprichst"""
    verb = _get_verb("sprechen")
    result = conjugate_präsens(verb, "du")
    assert result == "sprichst"


def test_helfen_du():
    """Test helfen: du hilfst"""
    verb = _get_verb("helfen")
    result = conjugate_präsens(verb, "du")
    assert result == "hilfst"


# ============================================================================
# 2. Verbs requiring epenthetic "-e-"
# ============================================================================

def test_warten_du():
    """Test warten: du wartest"""
    verb = _get_verb("warten")
    result = conjugate_präsens(verb, "du")
    assert result == "wartest"


def test_warten_er():
    """Test warten: er wartet"""
    verb = _get_verb("warten")
    result = conjugate_präsens(verb, "er")
    assert result == "wartet"


def test_arbeiten_du():
    """Test arbeiten: du arbeitest"""
    verb = _get_verb("arbeiten")
    result = conjugate_präsens(verb, "du")
    assert result == "arbeitest"


def test_arbeiten_er():
    """Test arbeiten: er arbeitet"""
    verb = _get_verb("arbeiten")
    result = conjugate_präsens(verb, "er")
    assert result == "arbeitet"


def test_sich_verabreden_sie():
    """Test sich verabreden: sie verabredet"""
    verb = _get_verb("sich verabreden")
    result = conjugate_präsens(verb, "sie")
    assert result == "verabredet"


def test_sich_verabreden_du():
    """Test sich verabreden: du verabredest"""
    verb = _get_verb("sich verabreden")
    result = conjugate_präsens(verb, "du")
    assert result == "verabredest"


def test_mieten_du():
    """Test mieten: du mietest"""
    verb = _get_verb("mieten")
    result = conjugate_präsens(verb, "du")
    assert result == "mietest"


def test_antworten_er():
    """Test antworten: er antwortet"""
    verb = _get_verb("antworten")
    result = conjugate_präsens(verb, "er")
    assert result == "antwortet"


def test_kosten_du():
    """Test kosten: du kostest"""
    verb = _get_verb("kosten")
    result = conjugate_präsens(verb, "du")
    assert result == "kostest"


# ============================================================================
# 3. Separable verbs
# ============================================================================

def test_aufstehen_er():
    """Test aufstehen: er steht (prefix separated in sentences, but conjugation is just 'steht')"""
    verb = _get_verb("aufstehen")
    result = conjugate_präsens(verb, "er")
    assert result == "steht"


def test_aufstehen_du():
    """Test aufstehen: du stehst"""
    verb = _get_verb("aufstehen")
    result = conjugate_präsens(verb, "du")
    assert result == "stehst"


def test_ankommen_ich():
    """Test ankommen: ich komme"""
    verb = _get_verb("ankommen")
    result = conjugate_präsens(verb, "ich")
    assert result == "komme"


def test_ankommen_er():
    """Test ankommen: er kommt"""
    verb = _get_verb("ankommen")
    result = conjugate_präsens(verb, "er")
    assert result == "kommt"


def test_einladen_du():
    """Test einladen: du lädst (has vowel change)"""
    verb = _get_verb("einladen")
    result = conjugate_präsens(verb, "du")
    assert result == "lädst"


def test_einladen_er():
    """Test einladen: er lädt"""
    verb = _get_verb("einladen")
    result = conjugate_präsens(verb, "er")
    assert result == "lädt"


# ============================================================================
# 4. Reflexive verbs
# ============================================================================

def test_sich_freuen_du():
    """Test sich freuen: du freust"""
    verb = _get_verb("sich freuen")
    result = conjugate_präsens(verb, "du")
    assert result == "freust"


def test_sich_freuen_ich():
    """Test sich freuen: ich freue"""
    verb = _get_verb("sich freuen")
    result = conjugate_präsens(verb, "ich")
    assert result == "freue"


def test_sich_erinnern_ich():
    """Test sich erinnern: ich erinnere"""
    verb = _get_verb("sich erinnern")
    result = conjugate_präsens(verb, "ich")
    assert result == "erinnere"


def test_sich_erinnern_du():
    """Test sich erinnern: du erinnerst"""
    verb = _get_verb("sich erinnern")
    result = conjugate_präsens(verb, "du")
    assert result == "erinnerst"


def test_sich_entscheiden_du():
    """Test sich entscheiden: du entscheidest (epenthetic -e- + reflexive)"""
    verb = _get_verb("sich entscheiden")
    result = conjugate_präsens(verb, "du")
    assert result == "entscheidest"


def test_sich_erkälten_du():
    """Test sich erkälten: du erkältest (epenthetic -e- + reflexive)"""
    verb = _get_verb("sich erkälten")
    result = conjugate_präsens(verb, "du")
    assert result == "erkältest"


# ============================================================================
# 5. Combined cases (reflexive + separable)
# ============================================================================

def test_sich_anziehen_sie():
    """Test sich anziehen: sie zieht (reflexive + separable)"""
    verb = _get_verb("sich anziehen")
    result = conjugate_präsens(verb, "sie")
    assert result == "zieht"


def test_sich_anziehen_du():
    """Test sich anziehen: du ziehst"""
    verb = _get_verb("sich anziehen")
    result = conjugate_präsens(verb, "du")
    assert result == "ziehst"


def test_sich_vorstellen_ich():
    """Test sich vorstellen: ich stelle"""
    verb = _get_verb("sich vorstellen")
    result = conjugate_präsens(verb, "ich")
    assert result == "stelle"


def test_sich_vorstellen_er():
    """Test sich vorstellen: er stellt"""
    verb = _get_verb("sich vorstellen")
    result = conjugate_präsens(verb, "er")
    assert result == "stellt"


# ============================================================================
# 6. Regular verbs (sanity checks)
# ============================================================================

def test_machen_ich():
    """Test machen: ich mache (regular verb)"""
    verb = _get_verb("machen")
    result = conjugate_präsens(verb, "ich")
    assert result == "mache"


def test_machen_du():
    """Test machen: du machst (regular verb)"""
    verb = _get_verb("machen")
    result = conjugate_präsens(verb, "du")
    assert result == "machst"


def test_gehen_ich():
    """Test gehen: ich gehe (regular verb)"""
    verb = _get_verb("gehen")
    result = conjugate_präsens(verb, "ich")
    assert result == "gehe"


def test_gehen_er():
    """Test gehen: er geht (regular verb)"""
    verb = _get_verb("gehen")
    result = conjugate_präsens(verb, "er")
    assert result == "geht"


# ============================================================================
# 7. Modal verbs (special cases)
# ============================================================================

def test_können_du():
    """Test können: du kannst"""
    verb = _get_verb("können")
    result = conjugate_präsens(verb, "du")
    assert result == "kannst"


def test_müssen_er():
    """Test müssen: er muss"""
    verb = _get_verb("müssen")
    result = conjugate_präsens(verb, "er")
    assert result == "muss"


def test_wollen_du():
    """Test wollen: du willst"""
    verb = _get_verb("wollen")
    result = conjugate_präsens(verb, "du")
    assert result == "willst"

