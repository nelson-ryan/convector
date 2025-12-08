

This project used the 2025-11-01 Wikipedia dump; the file is directly available
[here (23GB).](https://dumps.wikimedia.org/enwiki/20251120/enwiki-20251120-pages-articles-multistream.xml.bz2)

Use wikipediaextractor.WikipediaExtractor

Crucially update the `extract.py` file with commit [ab8988e](https://github.com/attardi/wikiextractor/commit/ab8988ebfa9e4557411f3d4c0f4ccda139e18875) for compatibility with Python 3.12

```bash
time ../.venv/bin/python -m wikiextractor.WikiExtractor -b 1G --json ./enwiki-20251101-pages-articles-multistream.xml.bz2
```

I've tried normal extraction without options; this yields doc tags. Annoying.

Json gives a more comfortable breakdown of fields, including 'text'; is this good?

Running `--no-template`; this also has doc tags, though.

Start with `no--template` option, in the interest of time.
If I understand the templates correctly, they might simply include duplication;
this either adds nothing or makes for more dense clusters in the DBSCAN


Install spacy model "en_core_web_md"
```bash
python -m spacy download en_core_web_md
```

Word2Vec training on only one file took 10 minutes.
Four files took 40 minutes; it seems to be linear.

Expect the full training to take roughly 190 minutes.
Took 213 (just over 3.5 hours), but I admittedly stole some resources by using
the computer while it was running.
