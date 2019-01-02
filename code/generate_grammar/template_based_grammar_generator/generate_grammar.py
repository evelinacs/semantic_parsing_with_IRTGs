import sys
import re
from collections import defaultdict
from nltk.tree import ParentedTree
from correspondences import ud_4lang_dict

def read_tree(tree_file):
    tree_line = tree_file.readline()
    if tree_line == "":
        return None
    else:
        tree = ParentedTree.fromstring(tree_line)
        return tree


def read_dep(dep_file):
    dep_regex = re.compile(r"^([^(]+)\(([^-]+)-\d+, ([^-]+)-\d+\)") # for lines like this: dep(side-2, neither-1)
    dep_list = []
    dep_line = dep_file.readline()
    while dep_line != "----------\n":
        if re.match(r"[a-zA-Z]", dep_line):
            if not dep_line.startswith("root"): # there's no root node in a tree
                dep_line = dep_regex.sub(r"\1, \2, \3", dep_line)
                dep_list.append(dep_line.strip())
        dep_line = dep_file.readline()
    return dep_list


def find_dep_tree_correspondences(tree, dep, seen):
    seen_ternary_nodes = defaultdict(dict)
   
    tree_dict = {} # index the tree by the words
    for smallest_subtree in tree.subtrees(lambda t: 2 == t.height()):
        tree_dict[smallest_subtree[0]] = smallest_subtree

    for subtree in tree.subtrees(lambda t: len(t) == 1 and 2 < t.height()): # unary subtrees
        template_params = {"treenode": subtree.label()}
        rtg_type = "{phrase} -> _{phrase}_unary_{arg}({arg})".format(
            phrase=subtree.label(),
            arg=subtree[0].label()
        )
        if rtg_type not in seen:
            print_rule("unary", template_params, rtg_type)
            seen.add(rtg_type)

    for current_dep in dep:
        dep_list = re.split(r', ', current_dep)
        dep_list[0] = dep_list[0].replace(":", "_")

        word1 = dep_list[1]
        word2 = dep_list[2]

        subtree1 = tree_dict[word1]
        subtree2 = tree_dict[word2]

        ancestor_info = find_common_ancestor(subtree1, subtree2)
        if ancestor_info["arity"] == 3:
            find_first_adjacent_dep(ancestor_info["common_ancestor"], seen_ternary_nodes, dep)

        template_params = {}
        template_params["treechildren"] = "?1, ?2" # overwritten later if not true (when merging ternaries)
        template_params["treenode"] = ancestor_info["common_ancestor"].label() + str(ancestor_info["arity"])
    

        template_name = ""
        if ancestor_info["arity"] == 2: # binary and ternary subtrees
            template_name += "binary_"
        elif ancestor_info["arity"] == 3:
            template_name += handle_ternary(template_params, ancestor_info, seen_ternary_nodes)
        
        template_name += "udnormal_"
        template_params["ud_edge"] = dep_list[0]
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

        if "ternary_phrase" in ancestor_info:
            rtg_phrase = ancestor_info["ternary_phrase"]
        else:
            rtg_phrase = ancestor_info["common_ancestor"].label()
        
        replace_arg = None
        if "ternary_arg" in ancestor_info: # happens when merging a ternary tree
            ancestor_hash = get_tree_hash(ancestor_info["common_ancestor"])
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
        
        rtg_type = "{phrase} -> _{treenode}_{dep}_{arg1}_{arg2}({arg1}, {arg2})".format(
            treenode=ancestor_info["common_ancestor"].label() + str(ancestor_info["arity"]),
            phrase=rtg_phrase,
            dep=dep_list[0],
            arg1=rtg_arg1, 
            arg2=rtg_arg2
        )

        if rtg_type not in seen:
            seen.add(rtg_type)

            print_rule(template_name, template_params, rtg_type)

def handle_4lang_case(template_params, deps, current_dep, is_reverse):
    template_name = "4langnormal"
    case_head = current_dep[1]
    for d in deps:
        dep_list = d.split(", ")
        if case_head == dep_list[2]:
            if dep_list[0] in ["nmod", "nmod:poss", "nmod:of"]:
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
        elif case_head == dep_list[1] and dep_list[0] != "case":
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
    node_hash = get_tree_hash(node)
    return seen_ternary_nodes[node_hash].get("seen", False)

def handle_ternary(template_params, ancestor_info, seen_ternary_nodes):
    common_ancestor = ancestor_info["common_ancestor"]
    technical_node = common_ancestor.label() + "_MERGE" 
    if ancestor_info["is_adjacent"] and not is_ternary_node_seen(seen_ternary_nodes, common_ancestor):
        ancestor_hash = get_tree_hash(common_ancestor)
        seen_ternary_nodes[ancestor_hash]["seen"] = True
        template_name = "ternary_"
        ancestor_info["ternary_phrase"] = technical_node
        if ancestor_info["is_leading_merge"]:
            template_params["treechildren"] = "?1, ?2, *"
        else:
            template_params["treechildren"] = "*, ?1, ?2"
    else:
        template_name = "binary_"
        ancestor_info["ternary_arg"] = technical_node
        template_params["treenode"] = "@"
    
    return template_name

def find_first_adjacent_dep(treenode, seen_ternary_nodes, deps):
    """
    Finds the first adjacent dependency link between the children of a ternary treenode
    """
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
    return treenode.pformat(100000)

def find_common_ancestor(subtree1, subtree2):
    pos_tuple1 = subtree1.treeposition()
    pos_tuple2 = subtree2.treeposition()
    common_ancestor = subtree1.root()

    for pos1, pos2 in zip(pos_tuple1, pos_tuple2):
        if pos1 == pos2:
            common_ancestor = common_ancestor[pos1]
        else:
            break
    
    arity = len(common_ancestor)
    is_adjacent = abs(pos1 - pos2) == 1

    result = {
        "common_ancestor": common_ancestor,
        "is_reverse": pos1 > pos2,
        "child1": common_ancestor[pos1],
        "child2": common_ancestor[pos2],
        "arity": arity,
        "is_adjacent": is_adjacent,
        "is_leading_merge": pos1 == 0 or pos2 == 0,
    }

    return result

def print_rule(template_name, template_params, rtg_type):
    with open("templates/{}.tpl".format(template_name), "r") as tpl_file:
        template = tpl_file.read()

        print(rtg_type)
        print(template.format(**template_params))
    


def main(fn1, fn2):
    seen = set() # keep track of rules to prevent duplicates
    print("interpretation string: de.up.ling.irtg.algebra.StringAlgebra")
    print("interpretation tree: de.up.ling.irtg.algebra.TagTreeAlgebra")
    print("interpretation ud: de.up.ling.irtg.algebra.graph.GraphAlgebra")
    print("interpretation fourlang: de.up.ling.irtg.algebra.graph.GraphAlgebra")
    print()
    print("S! -> sentence(NP)")
    print("[string] ?1")
    print("[tree] ?1")
    print("[ud] ?1")
    print("[fourlang] ?1")
    print()
    with open(fn1) as tree_file, open(fn2) as dep_file:
        while True:
            tree = read_tree(tree_file)
            if tree == None:
                break
            dep = read_dep(dep_file)
            find_dep_tree_correspondences(tree, dep, seen)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])


