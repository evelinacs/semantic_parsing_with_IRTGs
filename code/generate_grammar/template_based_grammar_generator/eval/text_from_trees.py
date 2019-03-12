import sys
from nltk.tree import Tree

def get_text_from_trees(fn):
    """
    Extracts raw text from Penn Treebank format
    """
    np_list = []
    with open(fn) as tree_file:
        for line in tree_file:
            tree = Tree.fromstring(line)
            words = tree.leaves()
            np_list.append(words)
    for sublist in np_list:
        print(*sublist[:-1]) # to remove the dot

get_text_from_trees(sys.argv[1])
