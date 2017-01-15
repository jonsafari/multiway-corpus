# Multiway Corpus

This builds an *n*-way multilingual corpus, from the data in the awesome [Tatoeba](http://tatoeba.org) dataset.
This allows you to do pivot-free [zero-shot](https://arxiv.org/abs/1611.04558) machine translation, as well as have unusual language combinations.

Usage is:

    python3 tatoeba_intersect.py Spanish jpn English

The arguments are the languages that you want to intersect, either the [ISO 639-3](data/lang_codes_iso-639-3.tsv) names (eg. English) or codes (eg. `eng`).
The output in this example will be `corpus.jpn`, `corpus.spa`, and `corpus.eng` .

First download two files into this directory, as these are constantly being updated upstream:

```bash
wget -c http://downloads.tatoeba.org/exports/sentences.tar.bz2  &&  tar jxvf sentences.tar.bz2
wget -c http://downloads.tatoeba.org/exports/links.tar.bz2      &&  tar jxvf links.tar.bz2
```

Then run the script.  Enjoy!

Here are some languages in the upstream dataset:

| Language | ISO 639-3 Code | Sentences |
| --- | --- | --- |
| English | eng | 641421 |
| Esperanto | epo | 511221 |
| Turkish | tur | 503109 |
| Russian | rus | 479397 |
| Italian | ita | 474880 |
| German | deu | 366934 |
| French | fra | 315677|
| Spanish | spa | 265058 |
| Portuguese | por | 231807 |
| Hungarian | hun | 191328 |
| Japanese | jpn | 184296 |
| Hebrew | heb | 153655 |
| Berber | ber | 104842 |
| (Hundreds more languages) | | |
