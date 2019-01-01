import sys
import re
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

        template_params = {}
        template_params["treenode"] = ancestor_info["common_ancestor"].label() + str(ancestor_info["arity"])
    

        template_name = ""
        if ancestor_info["arity"] == 2: # binary and ternary subtrees
            template_name += "binary_"
        elif ancestor_info["arity"] == 3:
            template_name += "ternary_"
        
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
            if fourlang_edge_type == "DOUBLE":
                template_name += "4langdouble"
                template_params["4lang_edge"] = "1"
                template_params["4lang_edge2"] = "2"
                template_params["4lang_dep1"] = "?1"
                template_params["4lang_dep2"] = "?2"

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

                

        if ancestor_info["is_reverse"] == True:
            rtg_type = "{phrase} -> _{treenode}_{dep}_{arg1}_{arg2}({arg1}, {arg2})".format(
                treenode=ancestor_info["common_ancestor"].label() + str(len(ancestor_info["common_ancestor"])),
                phrase=ancestor_info["common_ancestor"].label(),
                dep=dep_list[0],
                arg1=ancestor_info["child2"].label(), 
                arg2=ancestor_info["child1"].label())
        else:
            rtg_type = "{phrase} -> _{treenode}_{dep}_{arg1}_{arg2}({arg1}, {arg2})".format(
                treenode=ancestor_info["common_ancestor"].label() + str(len(ancestor_info["common_ancestor"])),
                phrase=ancestor_info["common_ancestor"].label(),
                dep=dep_list[0],
                arg1=ancestor_info["child1"].label(),
                arg2=ancestor_info["child2"].label())

        if rtg_type not in seen:
            seen.add(rtg_type)

            print_rule(template_name, template_params, rtg_type)

def find_common_ancestor(subtree1, subtree2):
    pos_tuple1 = subtree1.treeposition()
    pos_tuple2 = subtree2.treeposition()
    common_ancestor = subtree1.root()

    for pos1, pos2 in zip(pos_tuple1, pos_tuple2):
        if pos1 == pos2:
            common_ancestor = common_ancestor[pos1]
        else:
            break

    result = {
        "common_ancestor": common_ancestor,
        "is_reverse": pos1 > pos2,
        "child1": common_ancestor[pos1],
        "child2": common_ancestor[pos2],
        "arity": len(common_ancestor),
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

