import sys
import re
from collections import defaultdict
from nltk.tree import ParentedTree
from correspondences import ud_4lang_dict

def read_tree(tree_file):
    """
    Reads a single tree (line) from the given file
    """
    tree_line = tree_file.readline()
    if tree_line == "": # returns None when the end of the file is found
        return None
    else: # parses the line as a parented tree structure
        tree = ParentedTree.fromstring(tree_line)
        return tree


def read_dep(dep_file):
    """
    Reads all the dependencies for a single parsed tree
    """
    dep_regex = re.compile(r"^([^(]+)\(([^-]+)-\d+, ([^-]+)-\d+\)") # for lines like this: dep(side-2, neither-1)
    dep_list = []
    dep_line = dep_file.readline()
    while dep_line != "----------\n": # lines like this mark the end of the dependencies for a tree
        if re.match(r"[a-zA-Z]", dep_line):
            if not dep_line.startswith("root"): # there's no root node in a tree
                dep_line = dep_regex.sub(r"\1, \2, \3", dep_line) # converts lines like this:  dep(side-2, neither-1) to dep, side, neither
                dep_list.append(dep_line.strip())
        dep_line = dep_file.readline()
    return dep_list


def find_dep_tree_correspondences(tree, dep, seen):
    """
    Handles IRTG rule generation given a tree and its corresponding dependencies
    """
    seen_ternary_nodes = defaultdict(dict) # keeps track of ternary nodes in the tree to generate normal or merge rules for ternaries
   
    tree_dict = {} # index the tree by the words
    for smallest_subtree in tree.subtrees(lambda t: 2 == t.height()): # finds the smallest subtrees, e.g. (NNS students)
        tree_dict[smallest_subtree[0]] = smallest_subtree

    for subtree in tree.subtrees(lambda t: len(t) == 1 and 2 < t.height()): # unary subtrees, e.g. (NP (NNS students))
        template_params = {"treenode": subtree.label()} # holds values used in the template files
        rtg_type = "{phrase} -> _{phrase}_unary_{arg}({arg})".format(
            phrase=subtree.label(), # e.g. NP; left-hand side of the RTG rule
            arg=subtree[0].label() # e.g. DT, NN; right-hand side of the RTG rule
        )
        if rtg_type not in seen: # to avoid duplicates
            print_rule("unary", template_params, rtg_type)
            seen.add(rtg_type) # seen in main

    for current_dep in dep: # finds a corresponding tree structure for each dependency
        dep_list = re.split(r', ', current_dep)
        dep_list[0] = dep_list[0].replace(":", "_") # name of the dependency

        word1 = dep_list[1]
        word2 = dep_list[2]

        subtree1 = tree_dict[word1] # smallest subtree for the word
        subtree2 = tree_dict[word2]

        ancestor_info = find_common_ancestor(subtree1, subtree2)
        if ancestor_info["arity"] == 3: 
            find_first_adjacent_dep(ancestor_info["common_ancestor"], seen_ternary_nodes, dep) # for ternary nodes, finds which adjacent nodes are connected by a dependency first

        template_params = {}
        template_params["treechildren"] = "?1, ?2" # overwritten later if not true (when merging ternaries)
        template_params["treenode"] = ancestor_info["common_ancestor"].label() + str(ancestor_info["arity"]) # the node name in the tree interpretation
    

        template_name = ""
        if ancestor_info["arity"] == 2: # binary and ternary subtrees
            template_name += "binary_"
        elif ancestor_info["arity"] == 3:
            template_name += handle_ternary(template_params, ancestor_info, seen_ternary_nodes)
        
        template_name += "udnormal_"
        # Set some default template params; they will be overwritten if needed
        template_params["ud_edge"] = dep_list[0]
        # When the head of the dependency appears later in the tree than its dependent, the substituted arguments in the ud and 4lang interpretations must represent this difference in order
        if ancestor_info["is_reverse"] == True:
            template_params["ud_root"] = "?2"
            template_params["ud_dep"] = "?1"
            template_params["4lang_root"] = "?2"
            template_params["4lang_dep"] = "?1"
        else:
            template_params["ud_root"] = "?1"
            template_params["ud_dep"] = "?2"
            template_params["4lang_root"] = "?1"
            template_params["4lang_dep"] = "?2"


        # Checks if the dependency needs a special 4lang interpretation (edge type, node configuration, etc.)
        if dep_list[0] in ud_4lang_dict:
            fourlang_edge_type = ud_4lang_dict[dep_list[0]]
            #if fourlang_edge_type in ["0,0", "1,0"]:
            #    template_name += ...
            #NPs don't contain such edges, should be handled later
            if fourlang_edge_type == "CASE":
                template_name += handle_4lang_case(template_params, dep, dep_list, ancestor_info["is_reverse"])

            elif fourlang_edge_type == "HAS":
                template_name += "4langhas"
                template_params["4lang_edge"] = "1"
                template_params["4lang_edge2"] = "2"

            else:
                template_name += "4langnormal"
                template_params["4lang_edge"] = fourlang_edge_type


        else:
            # Checks if some nodes should be ignored in the 4lang interpretation
            if dep_list[0] in ["det", "punct"]: # this should be in a separate function later
                template_name += "4langignore"
                if ancestor_info["child1"].label() in ["DT", "PUNCT"]: # various punct tags should be handled later
                    if ancestor_info["is_reverse"]:
                        template_params["4langnode"] = "?1"
                    else:
                        template_params["4langnode"] = "?2"
                else:
                    if ancestor_info["is_reverse"]:
                        template_params["4langnode"] = "?2"
                    else:
                        template_params["4langnode"] = "?1"
            else:
                template_name += "4langnormal"
                template_params["4lang_edge"] = "_"

                
        # RTG rule generation

        # if ternary_phrase is set in ancestor_info, we have a ternary rule and the left-hand side needs to be replaced with the previously generated technical node name
        if "ternary_phrase" in ancestor_info:
            rtg_phrase = ancestor_info["ternary_phrase"]
        else:
            rtg_phrase = ancestor_info["common_ancestor"].label()
        
        replace_arg = None
        # Performs a check whether an RTG argument has to be replaced with a technical node name when merging a ternary tree
        if "ternary_arg" in ancestor_info: # happens when merging a ternary tree
            ancestor_hash = get_tree_hash(ancestor_info["common_ancestor"])
            # Decides which argument to replace based on which nodes were first connected by a dependency
            if seen_ternary_nodes[ancestor_hash]["is_leading_merge"]:
                replace_arg = 1
            else:
                replace_arg = 2
                template_params["treechildren"] = "?2, ?1"

        # set default rtg args
        if ancestor_info["is_reverse"] == True:
            rtg_arg1 = ancestor_info["child2"].label()
            rtg_arg2 = ancestor_info["child1"].label()
        else:
            rtg_arg1 = ancestor_info["child1"].label()
            rtg_arg2 = ancestor_info["child2"].label()
        
        # overwrite rtg args when merging a ternary tree
        if replace_arg == 1:
            rtg_arg1 = ancestor_info["ternary_arg"]
        elif replace_arg == 2:
            rtg_arg2 = ancestor_info["ternary_arg"]
        
        # Generate RTG rule line
        rtg_type = "{phrase} -> _{treenode}_{dep}_{arg1}_{arg2}({arg1}, {arg2})".format(
            treenode=ancestor_info["common_ancestor"].label() + str(ancestor_info["arity"]),
            phrase=rtg_phrase,
            dep=dep_list[0],
            arg1=rtg_arg1, 
            arg2=rtg_arg2
        )

        if rtg_type not in seen:
            # print the rule if it was not created previously
            seen.add(rtg_type)

            print_rule(template_name, template_params, rtg_type)

def handle_4lang_case(template_params, deps, current_dep, is_reverse):
    """
    Calculates information relating to the case dependency for the 4lang interpretation
    """
    template_name = "4langnormal"
    case_head = current_dep[1]
    # Finds a relevant dependency connected to this case dependency (it never appears alone)
    for d in deps:
        dep_list = d.split(", ")
        # Cases where the head of the case dep is the dependent of the related dependeny
        if case_head == dep_list[2]:
            if dep_list[0] in ["nmod", "nmod:poss", "nmod:of"]: # cases where a node is not represented in 4lang
                template_name = "4langignore"
                if is_reverse:
                    template_params["4langnode"] = "?2"
                else:
                    template_params["4langnode"] = "?1"
            elif dep_list[0] in ["obl", "nmod:in", "nmod:to"]:
                template_name = "4langnormal"
                template_params["4lang_edge"] = "2"
                if is_reverse:
                    template_params["4lang_root"] = "?1"
                    template_params["4lang_dep"] = "?2"
                else:
                    template_params["4lang_root"] = "?2"
                    template_params["4lang_dep"] = "?1"
        elif case_head == dep_list[1] and dep_list[0] != "case": # Cases where the head of the case dep is the head of the related dependeny (case dependencies should be ignored)
            if dep_list[0] == "nsubj":
                template_name = "4langnormal"
                template_params["4lang_edge"] = "1"
                if is_reverse:
                    template_params["4lang_root"] = "?1"
                    template_params["4lang_dep"] = "?2"
                else:
                    template_params["4lang_root"] = "?2"
                    template_params["4lang_dep"] = "?1"

    return template_name

def is_ternary_node_seen(seen_ternary_nodes, node):
    """
    Checks whether the "seen" flag has been set for a given node in seen_ternary_nodes
    """
    node_hash = get_tree_hash(node)
    return seen_ternary_nodes[node_hash].get("seen", False)

def handle_ternary(template_params, ancestor_info, seen_ternary_nodes):
    """
    Calculates information related to ternary node rules
    """
    common_ancestor = ancestor_info["common_ancestor"]
    technical_node = common_ancestor.label() + "_MERGE" # technical node name used in the left and right-hand side of the RTG rules handling ternary nodes
    
    """
    If the connected nodes are adjacent and the parent has not been processed yet,
    signal that a rule needs to be created that creates a ternary node in the tree interpretation.
    Otherwise a binary merge rule needs to be created later.
    Also some relating information needs to be calculated.
    """
    if ancestor_info["is_adjacent"] and not is_ternary_node_seen(seen_ternary_nodes, common_ancestor):
        ancestor_hash = get_tree_hash(common_ancestor) 
        seen_ternary_nodes[ancestor_hash]["seen"] = True # Mark this node as seen
        template_name = "ternary_"
        ancestor_info["ternary_phrase"] = technical_node # in the ternary templates, the left-hand side phrase must be replaced with the technical node name

        # decide where to put the node in the ternary that will be merged later
        if ancestor_info["is_leading_merge"]:
            template_params["treechildren"] = "?1, ?2, *"
        else:
            template_params["treechildren"] = "*, ?1, ?2"
    else:
        template_name = "binary_"
        ancestor_info["ternary_arg"] = technical_node # in a merge rule, one of the RTG arguments must be replaced by this technical node
        template_params["treenode"] = "@" # the treenode in the template must be replaced by the merge operation
    
    return template_name

def find_first_adjacent_dep(treenode, seen_ternary_nodes, deps):
    """
    Finds the first adjacent dependency link between the children of a ternary treenode
    """
    # Get the list of words contained in each of the nodes children
    child1_leaves = treenode[0].leaves()
    child2_leaves = treenode[1].leaves()
    child3_leaves = treenode[2].leaves()

    treenode_hash = get_tree_hash(treenode)

    # iterate through all the dependecies in the tree and return as soon as the first link is found
    for d in deps:
        dep_list = d.split(", ")
        # there can only be an adjacent link if one of the dependecy words belong to the second child
        if dep_list[1] in child2_leaves or dep_list[2] in child2_leaves:
            if dep_list[1] in child1_leaves or dep_list[2] in child1_leaves:
                # the link is between the first and second child
                seen_ternary_nodes[treenode_hash]["is_leading_merge"] = True
                return
            elif dep_list[1] in child3_leaves or dep_list[2] in child3_leaves:
                # the link is between the second and the third child
                seen_ternary_nodes[treenode_hash]["is_leading_merge"] = False
                return


def get_tree_hash(treenode):
    """
    NLTK trees are not hashable, this calculates a "hash" as a workaround, so they can be keys in a dictionary
    """
    return treenode.pformat(100000) # it returns a string

def find_common_ancestor(subtree1, subtree2):
    """
    finds the common ancestor for the given subtrees and some other relevant information
    """
    # tuples of indexes representing the positions of the subtrees in the main tree
    pos_tuple1 = subtree1.treeposition()
    pos_tuple2 = subtree2.treeposition()
    common_ancestor = subtree1.root() # the root node must be a common ancestor

    # iterates through the position indexes simultaneously
    for pos1, pos2 in zip(pos_tuple1, pos_tuple2):
        if pos1 == pos2: # if the positions match, a new common ancestor is found along the tree
            common_ancestor = common_ancestor[pos1]
        else: # if the positions are different, the previously found common ancestor is the lowest common ancestor, stop iterating over the positions
            break
    
    arity = len(common_ancestor)
    is_adjacent = abs(pos1 - pos2) == 1 # for adjacent nodes pos1-pos2 is either 1 or -1

    result = {
        "common_ancestor": common_ancestor,
        "is_reverse": pos1 > pos2, # if pos1 > pos2, the head of the dependency appears later in the tree than its dependent (based on treeposition indexes)
        "child1": common_ancestor[pos1],
        "child2": common_ancestor[pos2],
        "arity": arity,
        "is_adjacent": is_adjacent,
        "is_leading_merge": pos1 == 0 or pos2 == 0, # whether the 1st two nodes are connected by the dependency in a ternary (when is_adjacent is True)
    }

    return result

def print_rule(template_name, template_params, rtg_type):
    with open("templates/{}.tpl".format(template_name), "r") as tpl_file:
        template = tpl_file.read()

        print(rtg_type)
        print(template.format(**template_params))
    


def main(fn1, fn2):
    seen = set() # keep track of rules to prevent duplicates
    # interpretation definitions
    print("interpretation string: de.up.ling.irtg.algebra.StringAlgebra")
    print("interpretation tree: de.up.ling.irtg.algebra.TagTreeAlgebra")
    print("interpretation ud: de.up.ling.irtg.algebra.graph.GraphAlgebra")
    print("interpretation fourlang: de.up.ling.irtg.algebra.graph.GraphAlgebra")
    print()
    # start rule for NPs
    print("S! -> sentence(NP)")
    print("[string] ?1")
    print("[tree] ?1")
    print("[ud] ?1")
    print("[fourlang] ?1")
    print()
    # iterates through trees and their corresponding dependencies
    with open(fn1) as tree_file, open(fn2) as dep_file:
        while True:
            tree = read_tree(tree_file)
            if tree == None:
                break
            dep = read_dep(dep_file) # reads dependencies for the next tree
            find_dep_tree_correspondences(tree, dep, seen) 

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])


