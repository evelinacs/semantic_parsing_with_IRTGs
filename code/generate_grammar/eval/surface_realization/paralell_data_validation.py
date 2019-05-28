#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:33:44 2019

@author: kovacsadam
"""
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
        return None, None
    else: # parses the line as a parented tree structure
        tree = ParentedTree.fromstring(tree_line)
        return tree, tree_line

def basic_read_dep(dep_file):
    """
    Reads all the dependencies for a single parsed tree
    """
    dep_dict = {}
    dep_line = dep_file.readline()
    dep_string = ""
    while dep_line != "----------\n": # lines like this mark the end of the dependencies for a tree
        if DEP_LINE_CHECK.match(dep_line):
            dependency = get_dep_from_line(dep_line)
            dep_dict[dependency["dep"]] = dependency
        dep_string += dep_line
        dep_line = dep_file.readline()
    return dep_dict, dep_string


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

            tree, tree_string = basic_read_tree(tree_file)
            if tree == None:
                break
            words_tree = tree.leaves()
            dep, dep_string = basic_read_dep(dep_file) # reads dependencies for the next tree
            dep_words = [i for i in dep]
            
            same_len = len(words_tree) == len(dep_words)
            yield tree_string, dep_string, same_len


def main(fn1, fn2):
    with open("validated_tree", "w") as out_fn1:
        with open("validated_dep", "w") as out_fn2:
            for tree, dep, same_len in basic_tree_dep_reader(fn1, fn2):
                if same_len:
                    out_fn1.write(tree)
                    out_fn2.write(dep)
                    out_fn2.write("----------\n")


main(sys.argv[1], sys.argv[2])
