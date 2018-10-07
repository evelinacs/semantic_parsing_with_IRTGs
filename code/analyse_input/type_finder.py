import sys
import re
from collections import defaultdict

""" Finds and counts the types of phrase structures.
Should be used on the output of
code/generate_input_from_trees/extract_subtrees.py, like this:
python3 type_finder.py input_file | sort -n -r
"""

def type_finder():
    replacer = re.compile(r"[a-zA-Z]+\)")
    type_dict = defaultdict(int)
    with open(sys.argv[1]) as tree_file:
        for line in tree_file:
            line = replacer.sub(")", line)
            type_dict[line] += 1
        for key in type_dict:
            print(type_dict[key], key, end="")

type_finder()
