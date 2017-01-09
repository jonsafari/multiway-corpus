# Multiway Corpus

This builds an *n*-way multilingual corpus, from the data in the awesome [Tatoeba](http://tatoeba.org) dataset.
It does so in an efficient way, starting with the smallest language.

Usage is:

    python3 tatoeba-intersect.py Japanese Swedish swa English

The arguments are the languages that you want to intersect, either the [ISO 639-3](data/lang_codes_iso-639-3.tsv) names (eg. English) or codes (eg. `eng`).
The output in this example will be `corpus.jpn`, `corpus.swe`, `corpus.swa`, and `corpus.eng` .

You'll first need to download two files (into this directory), as these are constantly being updated upstream:

* wget -c http://downloads.tatoeba.org/exports/sentences.tar.bz2
* wget -c http://downloads.tatoeba.org/exports/links.tar.bz2
