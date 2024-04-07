/**
 * Classes and predicates for working with Latin WordNet data.
 */

extensible predicate latinWordNet(
  string lemma, string pos, string morpho, string url, string prosody
);

newtype TWord =
  MkWord(string lemma, string pos, string morpho, string url, string prosody) {
    latinWordNet(lemma, pos, morpho, url, prosody)
  }

class Word extends TWord {
  string lemma;
  string pos;
  string morpho;
  string url;
  string prosody;

  Word() { this = MkWord(lemma, pos, morpho, url, prosody) }

  string pos() { result = pos }

  Morpho morpho() { result = morpho }

  string url() { result = url }

  string prosody() { result = prosody }

  string toString() { result = lemma }
}

class Morpho extends string {
  string pos;
  string degree;
  string number;
  string tense;
  string mood;
  string voice;
  string gender;
  string case;
  string declension;
  string stemvariation;

  Morpho() {
    exists(MkWord(_, _, this, _, _)) and
    pos = this.charAt(0) and
    degree = this.charAt(1) and
    number = this.charAt(2) and
    tense = this.charAt(3) and
    mood = this.charAt(4) and
    voice = this.charAt(5) and
    gender = this.charAt(6) and
    case = this.charAt(7) and
    declension = this.charAt(8) and
    stemvariation = this.charAt(9)
  }

  /**
   * Gets the part of speech, which is one of
   *
   *  - a: adjective
   *  - n: noun
   *  - p: pronoun
   *  - r: adverb
   *  - v: verb
   */
  string pos() { result = pos }

  /**
   * Gets the degree, which is one of
   *
   *  - 1: (?)
   *  - 3: impersonal verb
   *  - p: positive (adjective)
   *  - c: comparative (adjective)
   *  - s: superlative (adjective)
   *  - -: not applicable
   */
  string degree() { result = degree }

  /**
   * Gets the number, which is one of
   *
   *  - s: singular
   *  - p: plural
   *  - -: not applicable
   */
  string number() { result = number }

  /**
   * Gets the verb tense, which is one of
   *
   *  - p: present
   *  - r: perfect
   *  - -: not applicable
   */
  string tense() { result = tense }

  /**
   * Gets the mood, which is one of
   *
   *  - i: indicative
   *  - -: not applicable
   */
  string mood() { result = mood }

  /**
   * Gets the voice, which is one of
   *
   *  - a: active
   *  - d: deponent
   *  - -: not applicable
   */
  string voice() { result = voice }

  /**
   * Gets the gender, which is one of
   *
   * - a: adjective
   * - c: common
   * - f: feminine
   * - m: masculine
   * - n: neuter
   * - -: not applicable
   */
  string gender() { result = gender }

  /**
   * Gets the case, which is one of
   *
   *  - a: accusative
   *  - n: nominative
   *  - -: not applicable
   */
  string case() { result = case }

  /**
   * Gets the declension group, which is a number from 1 to 5.
   */
  int declension() { result = declension.toInt() }

  /**
   * Gets the stem variations, which is one of
   *
   *  - i: i-stem
   *  - g: g-stem
   *  - p: p-stem
   *  - r: r-stem
   *  - -: not applicable
   */
  string stemvariation() { result = stemvariation }
}
