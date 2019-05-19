import sys
from nltk.tree import Tree

def get_trees_from_stanford_output(fn):
    with open(fn) as stanford_file:
        tree_string = ""
        for line in stanford_file:
            if line.startswith("(") or line.startswith(" "):
                tree_string += line
            if line == "\n":
                if tree_string != "":
                    tree = Tree.fromstring(tree_string)
                    print(tree.pformat(10000000))
                    tree_string = ""

get_trees_from_stanford_output(sys.argv[1])

