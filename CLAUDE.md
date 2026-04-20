# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Nature of the repository

This is a personal [commonplace book](https://en.wikipedia.org/wiki/Commonplace_book) — a collection of notes, mostly hand-written Markdown. It is not a software project with a build/test/lint pipeline. Editorial tasks (adding a note, fixing a typo, reorganizing a section) will dominate over coding tasks.

Top-level layout:
- `religion/` — the bulk of the content: notes on scripture, Church Fathers, Jewish-Christian dialogue, individual authors (Newman, Lewis, Soloveitchik, Buber-Rosenzweig, Pitre, …). Entry point is `religion/README.md`.
- `religion/bible-verses.md` — one verse per chapter of every book of the Catholic Bible, each quoted in the original Hebrew/Aramaic/Greek, the Latin Vulgate, and the RSVCE English. This is the structural pattern — preserve it when adding verses.
- `religion/sayings/`, `religion/bible-reading-plans/` — thematic subfolders; follow their existing structure when extending.
- `languages/latin/` — a small, self-contained side project (see below), unrelated to the note-taking content.

## Fetching scripture quotations

`religion/get-verse.sh` is a helper used when adding to `bible-verses.md` and similar files. It takes a language code and a verse reference:

```bash
./religion/get-verse.sh heb    GEN.1.1         # Hebrew OT via api.bible (needs $API_BIBLE_KEY)
./religion/get-verse.sh gk-ot  GEN.1.1         # Greek Septuagint via api.bible
./religion/get-verse.sh la     joannes+3:16    # Clementine Vulgate via bible-api.com
```

The `heb` and `gk-ot` modes hit `api.scripture.api.bible` and require `API_BIBLE_KEY` to be set in the environment. The `la` mode has no auth. Reference formats differ between the two APIs (dotted `GEN.1.1` vs. `joannes+3:16`).

## The `languages/latin` sub-project

This is an unrelated experiment in encoding Latin morphology in CodeQL, with its own README. Key points for working on it:

- It is a CodeQL pack (`qlpack.yml` → `name: latin`). Queries need a CodeQL database to run against; any database works — a stub is provided in `languages/latin/db/`.
- Morphology data comes from [Latin WordNet](https://latinwordnet.exeter.ac.uk/) and is loaded as a CodeQL data extension (`latinwordnet.yml`, extensible `latinWordNet` in pack `latin`).
- `download_latinwordnet.py` regenerates `latinwordnet.yml` by paging through the WordNet API. Run it only when the upstream data needs refreshing; it prints to stdout, so redirect into `latinwordnet.yml`.
- `latin.ql` is the sample query; `Nouns.qll` / `LatinWordNet.qll` are the library layer.

## Commit conventions

- Personal account repo — commits must be authored with `xiemaisi@gmail.com` (see user-level guidance).
- Branch prefix `max/`.
- PR descriptions: lead with a 1–2 sentence summary paragraph, no "Summary" or "Test plan" headers.
