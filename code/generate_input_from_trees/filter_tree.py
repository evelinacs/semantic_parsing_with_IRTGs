#!/usr/bin/env python3

import sys
import argparse
from nltk.tree import ParentedTree

parser = argparse.ArgumentParser(description = "Extract subtrees from Penn Treebank")
parser.add_argument("-s", "--sanitized", action = "store_true", help = "for sanitized input")

args = parser.parse_args()

def filter_trees():
    """
    Filters trees which contains subtrees that have more than 3 children.
    Also removes trace subtrees.
    """
    with open(sys.argv[1]) as np_doc:
        if args.sanitized:
            trace_subtree_pos = "HYPHENNONEHYPHEN"
        else:
            trace_subtree_pos = "-NONE-"
            
        for line in np_doc:
            t = ParentedTree.fromstring(line)
            maxlen = 0
            found = False
            treeposition = []
            for subtree in t.subtrees():
                if subtree.label() == trace_subtree_pos:
                    parent = subtree.parent()
                    if parent is not None:
                        treeposition.append(subtree.treeposition())   
                    if parent.parent() is not None:
                        treeposition.append(parent.treeposition())
                    found = True
                width = len(subtree)
                if width > maxlen:
                    maxlen = width
            if found:
                treeposition.sort(key=len)
                
                for position in treeposition[::-1]:
                    del t[position]
    
            if maxlen <=3:
                if t.leaves():
                    print(t.pformat(10000000), end = "\n")
                
                
if __name__ == "__main__":
    filter_trees()
