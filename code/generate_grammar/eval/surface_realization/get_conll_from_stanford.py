import re
import sys

from nltk.tree import ParentedTree

DEP_LINE_CHECK = re.compile(r"^[a-zA-Z]")
DEP_LINE_REGEX = re.compile(r"^([^(]+)\(([^-]+-\d+'*), ([^-]+-\d+'*)\)") # for lines like this: dep(side-2, neither-1)


def basic_read_tree(tree_file):
    """
    Reads a single tree (line) from the given file
    """
    tree_line = tree_file.readline()
    if tree_line == "": # returns None when the end of the file is found
        return None
    else: # parses the line as a parented tree structure
        tree = ParentedTree.fromstring(tree_line)
        return tree

def basic_read_dep(dep_file):
    """
    Reads all the dependencies for a single parsed tree
    """
    dep_dict = {}
    dep_line = dep_file.readline()
    while dep_line != "----------\n": # lines like this mark the end of the dependencies for a tree
        if DEP_LINE_CHECK.match(dep_line):
            dependency = get_dep_from_line(dep_line)
            dep_dict[dependency["dep"]] = dependency
        dep_line = dep_file.readline()
    return dep_dict


def is_self_referencing(dep):
    """
    Self-referencing dependencies have an ' as the last character.
    """
    return dep["root"][-1] == "'" or dep["dep"][-1] == "'"


def get_dep_from_line(dep_line):
    dep_match = DEP_LINE_REGEX.match(dep_line)
    return {
        "root": dep_match.group(2)[dep_match.group(2).find("-") + 1:].replace("'", ""),
        "dep": dep_match.group(3),
        "name": dep_match.group(1),
    }


def basic_tree_dep_reader(tree_fn, dep_fn):
    with open(tree_fn) as tree_file, open(dep_fn) as dep_file:
        while True:

            tree = basic_read_tree(tree_file)
            if tree == None:
                break
            dep = basic_read_dep(dep_file) # reads dependencies for the next tree

            yield tree, dep 


def main(fn1, fn2):
    for tree, dep_dict in basic_tree_dep_reader(fn1, fn2):
        for i, smallest_subtree in enumerate(tree.subtrees(lambda t: 2 == t.height())):
            try:
                pos = smallest_subtree.label()
                word = smallest_subtree[0]
                word_id = str(i + 1)
                word_in_dep_file = "{}-{}".format(word, word_id) # e. g. director-3; in the output of the Stanford parser
                dep_head_id = dep_dict[word_in_dep_file]["root"]
                dep_edge = dep_dict[word_in_dep_file]["name"]
                
                fields = [
                    word_id,
                    word,
                    "_", # lemma
                    "_", # UD pos
                    pos,
                    "_",
                    dep_head_id,
                    dep_edge,
                    "_",
                    "_",
                ]

                print("\t".join(fields))
            except KeyError as e:
                print(tree.pformat(1000000))
                raise(e)
        print()

main(sys.argv[1], sys.argv[2])