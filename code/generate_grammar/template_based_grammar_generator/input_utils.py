import re
import pdb

from nltk.tree import ParentedTree

DEP_LINE_CHECK = re.compile(r"^[a-zA-Z]")
DEP_LINE_REGEX = re.compile(r"^([^(]+)\(([^-]+-\d+'?), ([^-]+-\d+'?)\)") # for lines like this: dep(side-2, neither-1)

RE_ISI_WORD = re.compile(r"\s*\(([^\s]+)\s+/\s+([^\s\)]+)")
RE_ISI_DEP_NAME = re.compile(r"\s*:([^\s]+)")
RE_ISI_SUBGRAPH_END = re.compile(r"\s*\)")


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


def isi_read_dep(dep_file):
    dep_list = []
    dep_line = dep_file.readline().strip()
    
    pos = 0
    max_pos = len(dep_line)
    word_stack = []  # keeps track of the current "root" word
    current_dep_name = None
    
    while pos < max_pos:
        # Try to match a word eg: "(word / word"
        word_match = RE_ISI_WORD.match(dep_line, pos=pos)
        if word_match:
            word = word_match.group(2)
            # If there is an edge, create a dependency with the current root
            if current_dep_name is not None:
                dep_list.append({
                    "root": word_stack[-1],
                    "dep": word,
                    "name": current_dep_name,
                })
                current_dep_name = None
            # Advance the position in the graph
            pos += len(word_match.group(0))
            # Mark the new word as the current root
            word_stack.append(word)
            continue
        
        # Try to match a dependency name
        dep_name_match = RE_ISI_DEP_NAME.match(dep_line, pos=pos)
        if dep_name_match:
            # Save this as an edge, so a dependency can be created with the
            # next word
            current_dep_name = dep_name_match.group(1)
            # Advance the position in the graph
            pos += len(dep_name_match.group(0))
            continue
        
        # Try to match the end of a subgraph
        graph_end_match = RE_ISI_SUBGRAPH_END.match(dep_line, pos=pos)
        if graph_end_match:
            # Remove the current root word when the end of the current subgraph
            # is found
            word_stack = word_stack[:-1]
            # Advance the position in the graph
            pos += len(graph_end_match.group(0))
            continue
    # print(dep_list)
    # pdb.set_trace()
    return dep_list

def make_default_conllu_structure(graph_data, word_id):
    if word_id not in graph_data:
        graph_data[word_id] = {
            "word": "",
            "deps": {},
        }

def conllu_read_dep(dep_file):
    dep_line = dep_file.readline()
    graph_data = {}
    while dep_line != '\n':
        fields = dep_line.split('\t')
        word_id = fields[0]
        dep_word = fields[1]
        root_word_id = fields[6]
        dep_name = fields[7]

        make_default_conllu_structure(graph_data, word_id)
        graph_data[word_id]["word"] = dep_word

        """
        for the root; store the edges with the root of the dependency
        """
        # Ignore :root dependencies
        if "0" != root_word_id:
            make_default_conllu_structure(graph_data, root_word_id)
            graph_data[root_word_id]["deps"][word_id] = dep_name

        dep_line = dep_file.readline()
    
    dep_list = []
    for root_word_id in graph_data:
        root_word = graph_data[root_word_id]["word"]
        root_deps = graph_data[root_word_id]["deps"]

        for dep_word_id in root_deps:
            dep_word = graph_data[dep_word_id]["word"]
            dep_name = root_deps[dep_word_id]

            dependency = {
                "root": "{}-{}".format(root_word, root_word_id),
                "dep": "{}-{}".format(dep_word, dep_word_id),
                "name": dep_name,
            }
            normalize_dep_name(dependency)
            dep_list.append(dependency)
    
    return dep_list


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
            # dep = isi_read_dep(dep_file) # reads dependencies for the next tree
            yield tree, dep 
