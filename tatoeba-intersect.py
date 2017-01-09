#!/usr/bin/env python3
# By Jon Dehdari, 2017

import os

code_freq_filename = os.path.join('data', 'lang_codes_iso-639-3_freq.tsv')
code_filename = os.path.join('data', 'lang_codes_iso-639-3.tsv')
codes = {}
codes_rev = {}

def main():
    import sys

    langs = sys.argv[1:]
    print(langs)

    with open(code_freq_filename) as code_freq_file:
        code_freq = code_freq_file.read().split()

    with open(code_filename) as code_file:
        for line in code_file:
            code, lang = line.rstrip().split('\t')
            codes[code] = lang
            codes_rev[lang] = code



if __name__ == '__main__':
    main()
