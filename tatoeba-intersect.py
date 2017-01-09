#!/usr/bin/env python3
# By Jon Dehdari, 2017

import os

code_freq_filename = os.path.join('data', 'lang_codes_iso-639-3_freq.tsv')
code_filename = os.path.join('data', 'lang_codes_iso-639-3.tsv')

codes = {}
codes_rev = {}
links = {}
sents = {}

def main():
    import sys

    langs = sys.argv[1:]
    lang_set = set(langs) # for random access later

    # ISO 639-3 frequencies, based on number of entries in Tatoeba dataset
    with open(code_freq_filename) as code_freq_file:
        code_freq = code_freq_file.read().split()

    # Bijective mapping between ISO 639-3 language codes and their (macro-)language name.  Eg. eng:'English'
    with open(code_filename) as code_file:
        for line in code_file:
            code, lang = line.rstrip().split('\t')
            codes[code] = lang
            codes_rev[lang] = code

    # Relations between translation sentences
    with open('links.csv') as link_file:
        ...

    # Translation sentences
    with open('sentences.csv') as sentences_file:
        for line in sentences_file:
            id, code, sent = line.split('\t')
            if code in lang_set:
                ...



if __name__ == '__main__':
    main()
