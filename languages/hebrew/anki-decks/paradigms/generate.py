import csv
import sys

try:
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

from tf.app import use

def main():
    print("Loading BHSA corpus (Text-Fabric)...")
    A = use('etcbc/bhsa', silent='deep')
    api = A.api
    F, L, T = api.F, api.L, api.T

    BINYAN_MAP = {
        'qal': 'Qal',
        'nif': 'Niphal',
        'piel': 'Piel',
        'pual': 'Pual',
        'hif': 'Hiphil',
        'hof': 'Hophal',
        'hit': 'Hitpael'
    }

    TENSE_MAP = {
        'perf': 'Perfect',
        'impf': 'Imperfect',
        'wayq': 'Wayyiqtol (Vav-Consecutive)',
        'impv': 'Imperative',
        'infc': 'Infinitive Construct',
        'infa': 'Infinitive Absolute',
        'ptca': 'Active Participle',
        'ptcp': 'Passive Participle'
    }

    def format_pgn(person, gender, number):
        p = person.replace('p', '') if person not in ('NA', 'unknown') else ''
        
        # Handle gender: 1st person or unspecified gender is Common ('c')
        if gender in ('unknown', 'NA', 'c') or p == '1':
            g = 'c'
        else:
            g = gender

        # Standardize singular / plural
        if number in ('s', 'sg', 'singular'):
            n = 's'
        elif number in ('p', 'pl', 'plural'):
            n = 'p'
        else:
            n = ''

        return f"{p}{g}{n}".strip()

    TARGET_STEMS = set(['qal', 'nif', 'piel', 'pual', 'hif', 'hof', 'hit'])
    TARGET_TENSES = set(['perf', 'impf'])

    cards = []
    seen_slots = set()

    all_words = F.otype.s('word')
    total_words = len(all_words)

    print(f"Analyzing {total_words:,} words in the Hebrew Bible...")

    def process_word(word):
        if F.pdp.v(word) != 'verb':
            return None

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

                # Extract root in native Hebrew UTF-8 characters
                raw_root = F.voc_lex_utf8.v(word)
                root = raw_root.replace('/', '').replace('=', '').replace('[', '').replace(']', '').strip()
                
                pointed_word = F.g_word_utf8.v(word)

                verse_node = L.u(word, otype='verse')[0]
                verse_ref = T.sectionFromNode(verse_node)
                pointed_verse_text = T.text(verse_node, fmt='text-orig-full')

                # Highlight the verb form in bold within the full verse
                if pointed_word in pointed_verse_text:
                    highlighted_verse = pointed_verse_text.replace(pointed_word, f"<b>{pointed_word}</b>", 1)
                else:
                    highlighted_verse = pointed_verse_text

                form_label = f"{BINYAN_MAP[stem]} {TENSE_MAP[tense]} {pgn}".strip()
                citation = f"{verse_ref[0]} {verse_ref[1]}:{verse_ref[2]}"

                front_content = f"{form_label} ({root})"
                back_content = f"{highlighted_verse} ({citation})"

                return {
                    'Front': front_content,
                    'Back': back_content
                }
        return None

    if HAS_RICH:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
        ) as progress:
            task = progress.add_task("[cyan]Scanning verb forms...", total=total_words)
            for word in all_words:
                card = process_word(word)
                if card:
                    cards.append(card)
                    progress.update(task, description=f"[cyan]Cards generated: [bold green]{len(cards)}[/bold green]")
                progress.update(task, advance=1)
    else:
        for idx, word in enumerate(all_words):
            if idx % 50000 == 0 and idx > 0:
                print(f"Processed {idx:,} / {total_words:,} words... ({len(cards)} cards found)")
            card = process_word(word)
            if card:
                cards.append(card)

    output_filename = "hebrew_verb_paradigms.csv"
    with open(output_filename, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Front', 'Back'])
        writer.writeheader()
        writer.writerows(cards)

    print(f"\nDone! Exported {len(cards)} 2-column cards to '{output_filename}'.")

if __name__ == "__main__":
    main()