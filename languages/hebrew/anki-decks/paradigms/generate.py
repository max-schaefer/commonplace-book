import csv
import sys

# Try importing Rich for clean progress bars; fallback gracefully if not present
try:
    from rich.progress import (
        Progress,
        SpinnerColumn,
        TextColumn,
        BarColumn,
        TaskProgressColumn,
    )

    HAS_RICH = True
except ImportError:
    HAS_RICH = False

from tf.app import use


def main():
    print("Loading BHSA corpus (Text-Fabric)...")
    A = use("etcbc/bhsa", silent="deep")
    api = A.api
    F, L, T = api.F, api.L, api.T

    BINYAN_MAP = {
        "qal": "Qal",
        "nif": "Niphal",
        "piel": "Piel",
        "pual": "Pual",
        "hif": "Hiphil",
        "hof": "Hophal",
        "hit": "Hitpael",
    }

    TENSE_MAP = {
        "perf": "Perfect",
        "impf": "Imperfect",
        "wayq": "Wayyiqtol (Vav-Consecutive)",
        "impv": "Imperative",
        "infc": "Infinitive Construct",
        "infa": "Infinitive Absolute",
        "ptca": "Active Participle",
        "ptcp": "Passive Participle",
    }

    def format_pgn(person, gender, number):
        # Clean person string (e.g., 'p1' -> '1')
        p = person.replace("p", "") if person not in ("NA", "unknown") else ""

        # Handle gender: 1st person or unspecified gender is Common ('c')
        if gender in ("unknown", "NA", "c") or p == "1":
            g = "c"
        else:
            g = gender  # 'm' or 'f'

        # Standardize singular / plural
        if number in ("s", "sg", "singular"):
            n = "s"
        elif number in ("p", "pl", "plural"):
            n = "p"
        else:
            n = ""

        return f"{p}{g}{n}".strip()

    TARGET_STEMS = set(["qal", "nif", "piel", "pual", "hif", "hof", "hit"])
    TARGET_TENSES = set(["perf", "impf"])

    cards = []
    seen_slots = set()

    # Get total verb count for accurate progress tracking
    all_words = F.otype.s("word")
    total_words = len(all_words)

    print(f"Analyzing {total_words:,} words in the Hebrew Bible...")

    if HAS_RICH:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
        ) as progress:
            task = progress.add_task("[cyan]Scanning verb forms...", total=total_words)

            for idx, word in enumerate(all_words):
                if F.pdp.v(word) == "verb":
                    stem = F.vs.v(word)
                    tense = F.vt.v(word)
                    person = F.ps.v(word)
                    gender = F.gn.v(word)
                    number = F.nu.v(word)

                    if stem in TARGET_STEMS and tense in TARGET_TENSES:
                        pgn = format_pgn(person, gender, number)
                        slot_key = (stem, tense, pgn)

                        if slot_key not in seen_slots:
                            seen_slots.add(slot_key)

                            root = F.lex.v(word).replace("[", "").replace("=", "")
                            pointed_word = F.g_word_utf8.v(word)

                            verse_node = L.u(word, otype="verse")[0]
                            verse_ref = T.sectionFromNode(verse_node)

                            # Updated to correct Text-Fabric output format
                            pointed_verse_text = T.text(
                                verse_node, fmt="text-orig-full"
                            )

                            front_prompt = (
                                f"{BINYAN_MAP[stem]} {TENSE_MAP[tense]} {pgn}".strip()
                            )
                            citation = f"{verse_ref[0]} {verse_ref[1]}:{verse_ref[2]}"

                            cards.append(
                                {
                                    "Front_Prompt": front_prompt,
                                    "Hebrew_Form": pointed_word,
                                    "Root": root,
                                    "Verse_Citation": citation,
                                    "Verse_Hebrew": pointed_verse_text,
                                }
                            )
                            progress.update(
                                task,
                                description=f"[cyan]Cards generated: [bold green]{len(cards)}[/bold green]",
                            )

                progress.update(task, advance=1)
    else:
        # Fallback console logger if rich is not installed
        for idx, word in enumerate(all_words):
            if idx % 50000 == 0 and idx > 0:
                print(
                    f"Processed {idx:,} / {total_words:,} words... ({len(cards)} cards found)"
                )

            if F.pdp.v(word) == "verb":
                stem = F.vs.v(word)
                tense = F.vt.v(word)
                person = F.ps.v(word)
                gender = F.gn.v(word)
                number = F.nu.v(word)

                if stem in TARGET_STEMS and tense in TARGET_TENSES:
                    pgn = format_pgn(person, gender, number)
                    slot_key = (stem, tense, pgn)

                    if slot_key not in seen_slots:
                        seen_slots.add(slot_key)

                        root = F.lex.v(word).replace("[", "").replace("=", "")
                        pointed_word = F.g_word_utf8.v(word)

                        verse_node = L.u(word, otype="verse")[0]
                        verse_ref = T.sectionFromNode(verse_node)
                        pointed_verse_text = T.text(verse_node, fmt="text-orig-full")

                        front_prompt = (
                            f"{BINYAN_MAP[stem]} {TENSE_MAP[tense]} {pgn}".strip()
                        )
                        citation = f"{verse_ref[0]} {verse_ref[1]}:{verse_ref[2]}"

                        cards.append(
                            {
                                "Front_Prompt": front_prompt,
                                "Hebrew_Form": pointed_word,
                                "Root": root,
                                "Verse_Citation": citation,
                                "Verse_Hebrew": pointed_verse_text,
                            }
                        )

    # Export to CSV
    output_filename = "hebrew_verb_paradigms.csv"
    with open(output_filename, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "Front_Prompt",
                "Hebrew_Form",
                "Root",
                "Verse_Citation",
                "Verse_Hebrew",
            ],
        )
        writer.writeheader()
        writer.writerows(cards)

    print(f"\nDone! Exported {len(cards)} cards to '{output_filename}'.")


if __name__ == "__main__":
    main()
