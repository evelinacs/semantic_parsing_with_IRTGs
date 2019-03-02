import re

from nltk.tree import ParentedTree

DEP_LINE_CHECK = re.compile(r"^[a-zA-Z]")
DEP_LINE_REGEX = re.compile(r"^([^(]+)\(([^-]+-\d+'?), ([^-]+-\d+'?)\)") # for lines like this: dep(side-2, neither-1)


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
    dep_list = []
    dep_line = dep_file.readline()
    while dep_line != "----------\n": # lines like this mark the end of the dependencies for a tree
        if DEP_LINE_CHECK.match(dep_line):
            if not dep_line.startswith("root"): # there's no root node in a tree
                dependency = get_dep_from_line(dep_line)
                normalize_dep_name(dependency)
                if not is_self_referencing(dependency):
                    dep_list.append(dependency)
        dep_line = dep_file.readline()
    return dep_list


def is_self_referencing(dep):
    """
    Self-referencing dependencies have an ' as the last character.
    """
    return dep["root"][-1] == "'" or dep["dep"][-1] == "'"


def get_dep_from_line(dep_line):
    dep_match = DEP_LINE_REGEX.match(dep_line)
    return {
        "root": dep_match.group(2),
        "dep": dep_match.group(3),
        "name": dep_match.group(1),
    }


def normalize_dep_name(dep):
    dep["name"] = dep["name"].replace(":", "_") # : causes an error in Alto


def basic_tree_dep_reader(tree_fn, dep_fn):
    with open(tree_fn) as tree_file, open(dep_fn) as dep_file:
        while True:
            tree = basic_read_tree(tree_file)
            if tree == None:
                break
            dep = basic_read_dep(dep_file) # reads dependencies for the next tree
            yield tree, dep 
