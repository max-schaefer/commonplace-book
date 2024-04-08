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

class SecondDeclensionNoun extends Noun {
  string stem;

  SecondDeclensionNoun() {
    declension = 2 and
    (
      lemma = stem + "us"
      or
      lemma = stem + "um"
      or
      this.morpho().stemvariation() = "r" and lemma = stem
    )
  }

  override string form(string case, string number) {
    this.hasSingular() and
    number = "singular" and
    (
      case = "nominative" and result = lemma
      or
      case = "genitive" and result = stem + "i"
      or
      case = "dative" and result = stem + "o"
      or
      case = "accusative" and result = stem + "um"
      or
      case = "ablative" and result = stem + "o"
      or
      case = "vocative" and result = stem + "e"
    )
    or
    this.hasPlural() and
    number = "plural" and
    (
      case = "nominative" and result = stem + "i"
      or
      case = "genitive" and result = stem + "orum"
      or
      case = "dative" and result = stem + "is"
      or
      case = "accusative" and result = stem + "os"
      or
      case = "ablative" and result = stem + "is"
      or
      case = "vocative" and result = stem + "i"
    )
  }
}

class SecondDeclensionNounEndingInIus extends SecondDeclensionNoun {
  SecondDeclensionNounEndingInIus() { lemma.matches("%ius") }

  override string form(string case, string number) {
    if case = "vocative" and number = "singular"
    then result = stem + "i"
    else result = super.form(case, number)
  }
}

class NeuterSecondDeclensionNoun extends SecondDeclensionNoun {
  NeuterSecondDeclensionNoun() { gender = "n" }

  override string form(string case, string number) {
    // accusative and vocative are the same as nominative
    if case in ["accusative", "vocative"]
    then result = super.form("nominative", number)
    else
      // nominative plural ends in -a
      if case = "nominative" and number = "plural"
      then result = stem + "a"
      else
        // other cases are the same as masculine
        result = super.form(case, number)
  }
}

class SecondDeclensionRStemNoun extends SecondDeclensionNoun {
  SecondDeclensionRStemNoun() { this.morpho().stemvariation() = "r" }

  override string form(string case, string number) {
    if case = "vocative" and number = "singular"
    then result = lemma
    else result = super.form(case, number)
  }
}
