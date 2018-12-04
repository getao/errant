# -*- coding:utf-8 -*-

import argparse
import os
import spacy
from nltk.stem.lancaster import LancasterStemmer
import scripts.align_text as align_text
import scripts.cat_rules as cat_rules
import scripts.toolbox as toolbox
import nltk

parser = argparse.ArgumentParser(
    description="Convert parallel original and corrected text files (1 sentence per line) into M2 format.\nThe default uses Damerau-Levenshtein and merging rules and assumes tokenized text.",
    formatter_class=argparse.RawTextHelpFormatter,
    usage="%(prog)s [-h] [options] -orig ORIG -cor COR [COR ...] -out OUT")
parser.add_argument("-lev", help="Use standard Levenshtein to align sentences.", action="store_true")
parser.add_argument("-merge", choices=["rules", "all-split", "all-merge", "all-equal"], default="rules",
                    help="Choose a merging strategy for automatic alignment.\n"
                         "rules: Use a rule-based merging strategy (default)\n"
                         "all-split: Merge nothing; e.g. MSSDI -> M, S, S, D, I\n"
                         "all-merge: Merge adjacent non-matches; e.g. MSSDI -> M, SSDI\n"
                         "all-equal: Merge adjacent same-type non-matches; e.g. MSSDI -> M, SS, D, I")
global_args = parser.parse_args()
nlp = spacy.load("en")
# Lancaster Stemmer
stemmer = LancasterStemmer()
# GB English word list (inc -ise and -ize)
basename = os.path.dirname(os.path.realpath(__file__))
gb_spell = toolbox.loadDictionary(basename + "/resources/en_GB-large.txt")
# Part of speech map file
tag_map = toolbox.loadTagMap(basename + "/resources/en-ptb_map")

def extract(orig_sent, target_sent, args=global_args):

    orig_sent = orig_sent.decode('utf8')
    target_sent = target_sent.decode('utf8')
    # Markup the original sentence with spacy (assume tokenized)
    proc_orig = toolbox.applySpacy(orig_sent.split(), nlp)
    proc_target = toolbox.applySpacy(target_sent.split(), nlp)

    #print type(proc_target)

    #print proc_orig
    #print proc_target

    auto_edits = align_text.getAutoAlignedEdits(proc_orig, proc_target, nlp, args)
    res = []
    # Loop through the edits.
    for auto_edit in auto_edits:
        # Give each edit an automatic error type.
        cat = cat_rules.autoTypeEdit(auto_edit, proc_orig, proc_target, gb_spell, tag_map, nlp, stemmer)
        auto_edit[2] = cat
        edit_str = toolbox.formatEdit(auto_edit, 0)
        res.append(edit_str)
    return res


def main():
    raw_sentence = u"Google is accused of it ."
    crt_sentence = u"Google has been accused of it ."
    string1 = nltk.word_tokenize(raw_sentence)
    string2 = nltk.word_tokenize(crt_sentence)

    print extract(raw_sentence,crt_sentence)

#main()