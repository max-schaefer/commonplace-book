import LatinWordNet

class Noun extends Word {
  string gender;
  int declension;

  Noun() {
    this.pos() = "n" and
    gender = this.morpho().gender() and
    declension = this.morpho().declension()
  }

  predicate hasSingular() { this.morpho().number() = "s" }

  predicate hasPlural() {
    this.morpho().number() = "p"
    or
    // exclude singular proper nouns (starting with a capital letter)
    this.morpho().number() = "s" and
    not lemma.regexpMatch("^[A-Z].*")
  }

  abstract string form(string case, string number);
}

class FirstDeclensionNoun extends Noun {
  string stem;

  FirstDeclensionNoun() { declension = 1 and lemma = stem + "a" }

  override string form(string case, string number) {
    this.hasSingular() and
    number = "singular" and
    (
      case = "nominative" and result = stem + "a"
      or
      case = "genitive" and result = stem + "ae"
      or
      case = "dative" and result = stem + "ae"
      or
      case = "accusative" and result = stem + "am"
      or
      case = "ablative" and result = stem + "a"
      or
      case = "vocative" and result = stem + "a"
    )
    or
    this.hasPlural() and
    number = "plural" and
    (
      case = "nominative" and result = stem + "ae"
      or
      case = "genitive" and result = stem + "arum"
      or
      case = "dative" and result = stem + "is"
      or
      case = "accusative" and result = stem + "as"
      or
      case = "ablative" and result = stem + "is"
      or
      case = "vocative" and result = stem + "ae"
    )
  }
}

class Familia extends FirstDeclensionNoun {
  Familia() { lemma = "familia" }

  override string form(string case, string number) {
    result = super.form(case, number)
    or
    // older genitive singular
    case = "genitive" and number = "singular" and result = "familias"
  }
}

class FirstDeclensionFeminine extends FirstDeclensionNoun {
  FirstDeclensionFeminine() { gender = "f" }

  override string form(string case, string number) {
    result = super.form(case, number)
    or
    // dative/ablative plural to distinguish from masculine
    case in ["dative", "ablative"] and number = "plural" and result = stem + "abus"
  }
}
