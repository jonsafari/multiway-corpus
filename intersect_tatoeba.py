#!/usr/bin/env python3
# By Jon Dehdari, 2017

""" Builds an n-way multilingual corpus.  See the README.md for more details. """

import os
import sys

# Defaults
corpus_prefix = 'corpus.'
links_filename = 'links.csv'
sents_filename = 'sentences.csv'
code_freq_filename = os.path.join('data', 'lang_codes_iso-639-3_freq.tsv')
code_filename = os.path.join('data', 'lang_codes_iso-639-3.tsv')


def parse_lang_codes(code_filename):
    """
    Bijective mapping between ISO 639-3 language codes and their (macro-)language name.
    Eg. codes = {'eng':'English', ... }; codes_rev = {'English': 'eng', ...}
    """
    codes = {}
    codes_rev = {}
    with open(code_filename) as code_file:
        for line in code_file:
            code, lang = line.rstrip().split('\t')
            codes[code] = lang
            codes_rev[lang] = code
    return (codes, codes_rev)

def normalize_lang_codes(langs, codes, codes_rev):
    """ Normalize user-supplied langage names/codes to codes (eg. English to eng). """
    lang_set = set()
    for lang in langs:
        if lang in codes: # code is in ISO standard
            lang_set.add(lang)
        elif lang in codes_rev:
            lang_set.add(codes_rev[lang])
        else:
            print("Warning: \"%s\" is neither an ISO 639-3 code nor ISO 639-3 (macro-)language name.  I'll try anyways." % lang,
                  file=sys.stderr)
            lang_set.add(lang)
    return lang_set

def find_smallest_lang(code_freq_filename, lang_set):
    """
    Find language with fewest entries in Tatoeba dataset.
    This was already done to get code_freq_filename, using the following command:
    cut -f 2 sentences.csv | sort | uniq -c | sort -rn | tr -s ' ' |
      cut -d ' ' -f 3 > data/lang_codes_iso-639-3_freq.tsv
    """
    with open(code_freq_filename) as code_freq_file:
        code_freq = code_freq_file.read().split()
        smallest_lang_code = ''
        for code in code_freq:
            if code in lang_set:
                smallest_lang_code = code
    return smallest_lang_code

def get_smallest_lang_sents(sents_filename, smallest_lang_code, lang_set, lang_sent_ids):
    """
    Storing all translation sentences would be really memory inefficient,
    so we trade-off space for time, processing this file twice.  First we
    build-up a set of all sentence-id's for the smallest language.  Then, later,
    we pass through the file again, printing the sentence if it's a translation
    of one of the smallest language ID's.
    """
    smallest_lang_sents = {}
    with open(sents_filename) as sentences_file:
        for line in sentences_file:
            id, code, sent = line.rstrip().split('\t')
            id = int(id)
            if code in lang_set:
                lang_sent_ids[code].add(id)
                lang_sent_ids['All'].add(id)
            if code == smallest_lang_code: # this is a sentence from the smallest lang
                if id in smallest_lang_sents:
                    print("this shouldn't happen")
                else:
                    smallest_lang_sents[id] = {smallest_lang_code: sent}
    return smallest_lang_sents

def process_links(links_filename, lang_sent_ids):
    """ Relations between translation sentences. """
    links = {}
    with open(links_filename) as link_file:
        for line in link_file:
            key, val = line.rstrip().split('\t')
            key = int(key)
            val = int(val)
            # Ignore links that don't involve the languages we're interested in
            if key not in lang_sent_ids['All'] or val not in lang_sent_ids['All']:
                continue
            if key in links:
                links[key].add(val)
            else:
                links[key] = set([val])
    return links

def process_other_lang_sents(sents_filename, smallest_lang_code, lang_set,
                             links, smallest_lang_sents):
    """ See comments in get_smallest_lang_sents(). """
    with open(sents_filename) as sentences_file:
        for line in sentences_file:
            id, code, sent = line.rstrip().split('\t')
            id = int(id)
            if code in lang_set and code != smallest_lang_code and id in links:
                for small_id in links[id]:
                    # This takes the first translation, ignoring subsequent ones
                    if small_id in smallest_lang_sents and code not in smallest_lang_sents[small_id]:
                        smallest_lang_sents[small_id][code] = sent

def print_sents_to_files(lang_set, smallest_lang_sents, corpus_prefix):
    """ Opens, eg., corpus.{spa,eng}, prints parallel lines to respective
    files, and closes the files.
    """
    # Open all output files
    files = {}
    for code in lang_set:
        filename = corpus_prefix + code
        try:
            files[code] = open(filename, 'w')
        except OSError as err:
            print(err)

    # Now print sets that have all language translations
    output_sent_num = 0
    for _, val in smallest_lang_sents.items():
        if val.keys() == lang_set:
            output_sent_num += 1
            for lang, sent in val.items():
                print(sent, file=files[lang])

    # Close all output files
    for _, openfile in files.items():
        openfile.close()

    return output_sent_num


def main():
    """ Builds an n-way multilingual corpus. """
    langs = sys.argv[1:]

    codes, codes_rev = parse_lang_codes(code_filename)

    lang_set = normalize_lang_codes(langs, codes, codes_rev)

    # Initialize a set of ID's, for each language
    lang_sent_ids = {}
    lang_sent_ids['All'] = set()
    for lang in lang_set:
        lang_sent_ids[lang] = set()

    smallest_lang_code = find_smallest_lang(code_freq_filename, lang_set)

    lang_list_formatted = []
    for lang in lang_set:
        try:
            lang_list_formatted += ["%s (%s)" % (codes[lang], lang)]
        except:
            lang_list_formatted += ["%s" % lang]
    print("Looking for intersection of %s" % ', '.join(lang_list_formatted), file=sys.stderr)

    try:
        smallest_lang = codes[smallest_lang_code]
    except:
        smallest_lang = smallest_lang_code
    print("Processing sentences of smallest language, %s ..." %
          smallest_lang, file=sys.stderr, end=' ')
    smallest_lang_sents = get_smallest_lang_sents(sents_filename, smallest_lang_code,
                                                  lang_set, lang_sent_ids)
    print("%i entries" % len(smallest_lang_sents), file=sys.stderr)

    print("Processing links ...", file=sys.stderr)
    links = process_links(links_filename, lang_sent_ids)

    print("Processing sentences from the other specified languages ...", file=sys.stderr)
    process_other_lang_sents(sents_filename, smallest_lang_code, lang_set,
                             links, smallest_lang_sents)

    output_sent_num = print_sents_to_files(lang_set, smallest_lang_sents, corpus_prefix)

    # Pretty-print final message
    corpus_suffixes = ''
    for lang in lang_set:
        if corpus_suffixes == '':
            corpus_suffixes += lang
        else:
            corpus_suffixes += ',' + lang
    print("Output %i lines to:  %s{%s}" % (output_sent_num, corpus_prefix, corpus_suffixes),
          file=sys.stderr)


if __name__ == '__main__':
    main()
