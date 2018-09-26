#!/usr/bin/env python3

import sys
from nltk.tree import Tree

#Converts Penn Treebank to Alto-compatible format

phrase_levels = [
    "ADJP",
    "ADVP",
    "CONJP",
    "FRAG",
    "INTJ",
    "LST",
    "NAC",
    "NP",
    "NX",
    "PP",
    "PRN",
    "PRT",
    "QP",
    "RRC",
    "UCP",
    "VP",
    "WHADJP",
    "WHAVP",
    "WHNP",
    "WHPP",
    "X",
]

def format_tree():
    with open(sys.argv[1]) as np_doc:
        for line in np_doc:
            np = Tree.fromstring(line)
            print_tree(np)
            print()


def print_tree(tree):
    if tree.height() == 2:
        print("{}( {})".format(tree.label(), tree[0]), end="") #pos, word; Stanford format
    else:
        tree_len = len(tree)
        if tree.label() in phrase_levels and tree_len > 1: #NP2, NP3...
            tree.set_label("{}{}".format(tree.label(), tree_len))

        print("{}( ".format(tree.label()), end="")
        index = 1
        for subtree in tree:
            print_tree(subtree)
            if tree_len > index:
                print(", ", end="")
            index += 1
        print(")", end="")

if __name__ == "__main__":
    format_tree()
