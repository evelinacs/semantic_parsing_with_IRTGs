import sys

from utils import REPLACE_MAP
from utils import sanitize_word

from nltk.tree import Tree


def sanitize_label(tree): #sanitize labels which contain hyphens (e.g.NP-SBJ)
    for key in REPLACE_MAP:
        tree.set_label(tree.label().replace(key, REPLACE_MAP[key]))


def sanitize_tree(tree):
    sanitize_label(tree)
    if tree.height() == 2: #word, pos
        tree[0] = sanitize_word(tree[0]) #tree[0] == word
    else:
        for subtree in tree:
            sanitize_tree(subtree)


def get_text_from_trees(fn):
    """
    Extracts raw text from Penn Treebank format
    """
    np_list = []
    with open(fn) as tree_file:
        for line in tree_file:
            tree = Tree.fromstring(line)
            sanitize_tree(tree)

            words = tree.leaves()
            np_list.append(words)
    for sublist in np_list:
        print(*sublist[:-1]) # to remove the dot
            # print(tree.pformat(10000000))

get_text_from_trees(sys.argv[1])
