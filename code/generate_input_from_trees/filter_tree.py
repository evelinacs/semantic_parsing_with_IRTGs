#!/usr/bin/env python3

import sys
from nltk.tree import ParentedTree

def filter_trees():
    """
    Filters trees which contains subtrees that have more than 3 children.
    Also removes trace subtrees.
    """
    with open(sys.argv[1]) as np_doc:
        for line in np_doc:
            t = ParentedTree.fromstring(line)
            maxlen = 0
            found = False
            for subtree in t.subtrees():
                if subtree.label() == "-NONE-":
                    treeposition = subtree.treeposition()
                    found = True
                width = len(subtree)
                if width > maxlen:
                    maxlen = width
            if found:
                del t[treeposition]
            
            if maxlen <=3:
                print(t.pformat(1000000), end="")
                
                
if __name__ == "__main__":
    filter_width()