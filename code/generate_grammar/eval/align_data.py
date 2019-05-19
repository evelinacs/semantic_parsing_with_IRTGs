import sys
import re

from nltk.tree import ParentedTree

"""
Create parallel data from Penn Treebanks and those parsed by Parser v2.
"""

RE_WORD = re.compile(r"[^\( ]+\s+/\s+([^\s\)]+)")

def find_tree_words(t):
    return tuple(sorted(["{}-{}".format(leaf, i + 1) for i, leaf in enumerate(t.leaves())]))
    #return tuple(sorted(t.leaves()))


def find_dep_words(d):
    #words = re.findall("[\()]\w+", d)
    #words = [word.strip('(') for word in words]
    #return tuple(sorted(words))
    words = RE_WORD.findall(d)
    return tuple(sorted(words))


def tree_dep_reader(tree_fn, dep_fn):
    dep_dict = {}
    with open(tree_fn) as tree_file, open(dep_fn) as dep_file:
        for line in dep_file:
            dep_line = line
            dep_words = find_dep_words(line)
            dep_dict[dep_words] = dep_line
        for line in tree_file:
            tree = ParentedTree.fromstring(line)
            tree_words = find_tree_words(tree)
            if tree_words in dep_dict:
                print(dep_dict[tree_words], end='')
            else:
                print('<none>')



tree_dep_reader(sys.argv[1], sys.argv[2])