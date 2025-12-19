# German Language Data Audit Report
## A1–B1 Learner Correctness Audit

---

## ❌ ERROR: "treffen" (line 3-26)
**Issue**: `"reflexive": true` is incorrect.
**Explanation**: "treffen" (to meet) is NOT reflexive. "sich treffen" (to meet each other) is reflexive, but "treffen" alone takes a direct object: "Ich treffe den Freund" (I meet the friend). The reflexive form requires "sich" explicitly in the infinitive.

---

## ❌ ERROR: "arbeiten" (line 574-591)
**Issue**: `"irregular_present"` field exists but "arbeiten" is regular.
**Explanation**: "arbeiten" is a regular verb. Present tense: ich arbeite, du arbeitest, er/sie/es arbeitet. The forms listed are correct but not irregular. This field should not exist for regular verbs.

---

## ❌ ERROR: "mieten" (line 752-774)
**Issue**: `"irregular_present"` field exists but "mieten" is regular.
**Explanation**: "mieten" is a regular verb. Present tense: ich miete, du mietest, er/sie/es mietet. The forms listed are correct but not irregular.

---

## ❌ ERROR: "schicken" (line 1142-1158)
**Issue**: `"valency": "dat"` is misleading.
**Explanation**: "schicken" takes an accusative direct object (what you send) and optionally a dative indirect object (to whom). The primary valency should be "akk" for the direct object. The dative is secondary/optional. Example: "Ich schicke einen Brief (akk) dem Freund (dat)" or "Ich schicke dem Freund (dat) einen Brief (akk)".

---

## ❌ ERROR: "zeigen" (line 1160-1176)
**Issue**: `"valency": "dat"` is misleading.
**Explanation**: "zeigen" takes an accusative direct object (what you show) and optionally a dative indirect object (to whom). The primary valency should be "akk" for the direct object. Example: "Ich zeige dem Freund (dat) das Buch (akk)".

---

## ❌ ERROR: "studieren" (line 1335-1351)
**Issue**: `"allowed_objects"` includes `"an der Universität"` which is a prepositional phrase, not a direct object.
**Explanation**: "studieren" takes an accusative direct object (what you study: "Medizin", "Deutsch"). "an der Universität" is a prepositional phrase indicating location, not a direct object. This violates the valency pattern.

---

## ❌ ERROR: "beenden" (line 1408-1430)
**Issue**: `"irregular_present"` field exists but "beenden" is regular.
**Explanation**: "beenden" is a regular verb. Present tense: ich beende, du beendest, er/sie/es beendet. The forms listed are correct but not irregular.

---

## ❌ ERROR: "antworten" (line 1450-1472)
**Issue**: `"irregular_present"` field exists but "antworten" is regular.
**Explanation**: "antworten" is a regular verb. Present tense: ich antworte, du antwortest, er/sie/es antwortet. The forms listed are correct but not irregular.

---

## ⚠️ AMBIGUOUS: "passieren" (line 1552-1568)
**Issue**: `"valency": "dat"` and `"allowed_objects"` are misleading.
**Explanation**: "passieren" is an impersonal verb. Structure: "etwas (nom) passiert jemandem (dat)" (something happens to someone). The examples in `"allowed_objects"` show dative objects ("dem Freund", "der Freundin", "mir"), which is correct, but the verb's structure is unusual and the examples don't show the typical subject-object relationship. For A1–B1 learners, this could be confusing without context showing the full sentence structure.

---

## ❌ ERROR: "sich verabreden" (line 1731-1753)
**Issue**: `"irregular_present"` field exists but "verabreden" is regular.
**Explanation**: "verabreden" is a regular verb. Present tense: ich verabrede, du verabredest, er/sie/es verabredet. The forms listed are correct but not irregular.

---

## ❌ ERROR: "backen" (line 1833-1855)
**Issue**: `"irregular_present"` includes `"du": "bäckst"` which is archaic.
**Explanation**: Modern standard German uses "du backst" (regular form), not "bäckst". The form "bäckst" is archaic/regional. For A1–B1 learners, this is misleading and incorrect for standard German.

---

## ❌ ERROR: "sich erkälten" (line 1914-1931)
**Issue**: `"irregular_present"` field exists but "erkälten" is regular.
**Explanation**: "erkälten" is a regular verb. Present tense: ich erkälte, du erkältest, er/sie/es erkältet. The forms listed are correct but not irregular.

---

## ⚠️ AMBIGUOUS: "geben" (line 800-822)
**Issue**: `"valency": "dat"` is incomplete.
**Explanation**: "geben" takes both accusative (what) and dative (to whom) objects. The valency field only shows "dat", but the verb requires both cases. Example: "Ich gebe dem Freund (dat) das Buch (akk)". For A1–B1 learners, showing only dative could mislead them into thinking "geben" only takes dative.

---

## ⚠️ AMBIGUOUS: "bringen" (line 824-840)
**Issue**: `"valency": "dat"` is incomplete.
**Explanation**: "bringen" takes both accusative (what) and dative (to whom) objects. The valency field only shows "dat", but the verb requires both cases. Example: "Ich bringe dem Freund (dat) das Buch (akk)".

---

## ⚠️ AMBIGUOUS: "einladen" (line 1755-1777)
**Issue**: `"valency": "akk"` is incomplete.
**Explanation**: "einladen" can take both accusative (whom you invite) and optionally a prepositional phrase ("zu etwas"). The examples show only accusative objects, which is correct, but the verb can also be used with "zu" (e.g., "zu einer Party einladen"). For A1–B1 learners, this is acceptable but could be more complete.

---

## ⚠️ AMBIGUOUS: "erklären" (line 1432-1448)
**Issue**: `"valency": "dat"` is incomplete; `"allowed_objects"` only shows dative objects.
**Explanation**: "erklären" requires both accusative (what you explain) and dative (to whom) objects. Example: "Ich erkläre dem Freund (dat) die Grammatik (akk)". Showing only dative objects misleads learners about the verb's complete valency pattern.

---

## ⚠️ AMBIGUOUS: "erzählen" (line 1474-1490)
**Issue**: `"valency": "dat"` is incomplete; `"allowed_objects"` only shows dative objects.
**Explanation**: "erzählen" requires both accusative (what you tell) and dative (to whom) objects. Example: "Ich erzähle dem Freund (dat) eine Geschichte (akk)". Showing only dative objects misleads learners about the verb's complete valency pattern.

---

## Summary

**Total Errors Found**: 12
**Total Ambiguous Items**: 6

**Error Categories**:
- Incorrect reflexivity: 1
- Incorrect valency marking: 3
- Incorrect irregular_present fields: 6
- Incorrect object examples: 1
- Archaic form: 1

**Ambiguous Categories**:
- Incomplete valency information: 5
- Unusual verb structure: 1

