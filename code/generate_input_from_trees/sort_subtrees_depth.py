#!/usr/bin/env python3

import sys
from nltk.tree import Tree

def sort_subtrees_depth():
    with open(sys.argv[1]) as subtree_doc:
        for line in subtree_doc:
            subtree = Tree.fromstring(line)
            print(subtree.height(), line, end ="")

if __name__ == "__main__":
    sort_subtrees_depth()
