import sys
import argparse

from nltk.corpus import treebank

from utils import REPLACE_MAP
from utils import sanitize_word
from ptb import ptb

parser = argparse.ArgumentParser(description = "Extract subtrees from Penn Treebank")
parser.add_argument("phrase_level", type = str, help = "the name of the phrase level to extract, e.g. NP, ADJP")
parser.add_argument("-o", "--output_format", choices = ["stanford", "sanitized", "raw"], required = True, help = "format of the output")
parser.add_argument("-c", "--complete_ptb", action = "store_true", help = "Set to use the complete WSJ section of the PTB")


args = parser.parse_args()


def sanitize_label(tree): #sanitize labels which contain hyphens (e.g.NP-SBJ)
    for key in REPLACE_MAP:
        tree.set_label(tree.label().replace(key, REPLACE_MAP[key]))


def sanitize_tree(tree, output_format):
    if output_format == "raw":
        return
    if output_format == "sanitized":
        sanitize_label(tree)

    if tree.height() == 2: #word, pos
        tree[0] = sanitize_word(tree[0]) #tree[0] == word
    else:
        for subtree in tree:
            sanitize_tree(subtree, output_format)


def sanitize_pos(tree): #replace punctuation pos-tags
    tree_label = tree.label()
    is_punct = True
    for character in tree_label:
        if character not in REPLACE_MAP:
            is_punct = False
    if is_punct == True:
        tree.set_label("PUNCT")


def main(phrase_level, output_format, complete_ptb):
    iter_range = [1] if complete_ptb else range(1, 200)
    for n in iter_range:
        if complete_ptb:
            sentences = ptb.parsed_sents()
        else:
            tree_file = "wsj_{}.mrg".format(str(n).zfill(4))
            sentences = treebank.parsed_sents(tree_file)
        for s in sentences:
            for subtree in s.subtrees(lambda t: t.label() == phrase_level):
                sanitize_tree(subtree, output_format)
                print(subtree.pformat(100000))

if __name__ == "__main__":
    main(args.phrase_level, args.output_format, args.complete_ptb)
