#!/usr/bin/env python3

import sys
from nltk.tree import Tree

def filter_width():
    with open(sys.argv[1]) as np_doc:
        for line in np_doc:
            t = Tree.fromstring(line)
            width = len(t)
            if width <= 3:
                print(line, end = "")

if __name__ == "__main__":
    filter_width()