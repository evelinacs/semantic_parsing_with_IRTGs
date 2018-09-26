#!/usr/bin/env python3

import sys
from nltk.tree import Tree

def sort_subtrees_width():
    with open(sys.argv[1]) as subtree_doc:
        for line in subtree_doc:
            t = Tree.fromstring(line)
            width = len(t)
            print(width, line, end = "")

if __name__ == "__main__":
    sort_subtrees_width()