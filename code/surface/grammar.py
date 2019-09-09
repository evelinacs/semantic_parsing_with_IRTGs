import sys
import re
import copy
import operator
from collections import defaultdict, OrderedDict

ENGLISH_WORD = re.compile("^[a-zA-Z0-9]*$")

REPLACE_MAP = {
    ":": "COLON",
    ",": "COMMA",
    ".": "PERIOD",
    ";": "SEMICOLON",
    "-": "HYPHEN",
    "_": "DASH",
    "[": "LSB",
    "]": "RSB",
    "(": "LRB",
    ")": "RRB",
    "{": "LCB",
    "}": "RCB",
    "!": "EXC",
    "?": "QUE",
    "'": "SQ",
    '"': "DQ",
    "/": "PER",
    "\\": "BSL",
    "#": "HASHTAG",
    "%": "PERCENT",
    "&": "ET",
    "@": "AT",
    "$": "DOLLAR",
    "*": "ASTERISK",
    "^": "CAP",
    "`": "IQ",
    "+": "PLUS",
    "|": "PIPE",
    "~": "TILDE",
    "<": "LESS",
    ">": "MORE",
    "=": "EQ"
}

KEYWORDS = set(["feature"])


def make_default_structure(graph_data, word_id):
    if word_id not in graph_data:
        graph_data[word_id] = {
            "word": "",
            "deps": {},
        }


def add_unseen_rules(grammar, fn_dev):
    graph_data = {}
    noun_list = []
    with open(fn_dev, "r") as f:
        for i,line in enumerate(f):            
            if line == "\n":
                for w in graph_data:
                    for dep in graph_data[w]["deps"]:
                        edge_dep = graph_data[w]["deps"][dep]
                        to_pos = graph_data[dep]["tree_pos"]
                        mor = graph_data[dep]["mor"]
                            
                        if "tree_pos" in graph_data[w]:
                            line_key_before = graph_data[w]["tree_pos"] + ">" + to_pos + "|" + edge_dep + "&>"
                            line_key_after = graph_data[w]["tree_pos"] + ">>" + to_pos + "|" + edge_dep + "&"
                           
                            if "lin=+" in mor and line_key_after in grammar:
                                grammar[line_key_after] += 1
                            elif "lin=-" in mor and line_key_before in grammar:
                                grammar[line_key_before] += 1

                            if line_key_before not in grammar and line_key_after not in grammar:
                                if "lin=+" in mor:
                                    grammar[line_key_after] = 1
                                elif "lin=-" in mor:
                                    grammar[line_key_before] = 1                              
                                else:
                                    grammar[line_key_before] = 1
                                    grammar[line_key_after] = 1
                            elif line_key_before not in grammar:
                                grammar[line_key_before] = 1
                            elif line_key_after not in grammar:
                                grammar[line_key_after] = 1

                graph_data = {}
                noun_list = []
                continue
            if line != "\n":
                fields = line.split("\t")
                word_id = fields[0]
                word = fields[1]
                tree_pos = fields[3]
                ud_pos = fields[4]
                mor = fields[5]
                head = fields[6]
                ud_edge = fields[7]

                make_default_structure(graph_data, word_id)
                graph_data[word_id]["word"] = word
                graph_data[word_id]["tree_pos"] = sanitize_word(ud_pos)
                graph_data[word_id]["mor"] = mor

                make_default_structure(graph_data, head)
                graph_data[head]["deps"][word_id] = ud_edge


def train_edges(fn_train, fn_dev):
    graph_data = {}
    pos_to_count = defaultdict(lambda:1)

    with open(fn_train, "r") as f:
        for i,line in enumerate(f):
            if line.startswith("#"):
                continue
            if line == "\n":
                for w in graph_data:
                    for dep in graph_data[w]["deps"]:
                        if "tree_pos" in graph_data[w]:
                            line_key = ""
                            line_key += graph_data[w]["tree_pos"] + ">"
                    
                            if int(dep) < int(w):
                                edge = graph_data[w]["deps"][dep]
                                pos = graph_data[dep]["tree_pos"]
                                line_key += pos + "|" + edge + "&"
                                line_key += ">"
                                pos_to_count[line_key] += 1
                            elif int(dep) > int(w):
                                edge = graph_data[w]["deps"][dep]
                                pos = graph_data[dep]["tree_pos"]
                                line_key += ">"
                                line_key += pos + "|" + edge + "&"
                                pos_to_count[line_key] += 1

                graph_data = {}
                continue
            if line != "\n":
                fields = line.split("\t")
                word_id = fields[0]
                word = fields[1]
                tree_pos = fields[3]
                ud_pos = fields[4]
                mor = fields[5]
                head = fields[6]
                ud_edge = fields[7]

                make_default_structure(graph_data, word_id)
                graph_data[word_id]["word"] = word
                graph_data[word_id]["tree_pos"] = sanitize_word(ud_pos)
                graph_data[word_id]["mor"] = mor

                make_default_structure(graph_data, head)
                graph_data[head]["deps"][word_id] = ud_edge            
                
    sorted_x = sorted(pos_to_count.items(), key=operator.itemgetter(1), reverse=True)
    sorted_dict = OrderedDict(sorted_x)
    add_unseen_rules(sorted_dict, fn_dev)
    with open("train_edges", "w") as out_f:
        for pos in sorted_dict:
            w_from = pos.split(">")[0]
            w_before = pos.split(">")[1]
            w_after = pos.split(">")[2]
            out_f.write(w_from + "\t" + w_before.strip("&") + "\t" + w_after.strip("&") + "\t" + str(pos_to_count[pos]) + "\n")

           
def train_subgraphs(fn_train, fn_dev):
    graph_data = {}
    noun_list = []
    pos_to_count = defaultdict(lambda:1)

    with open(fn_train, "r") as f:
        for i,line in enumerate(f):
            if line.startswith("#"):
                continue
            if line == "\n":
                for w in graph_data:
                    nodes_before = []
                    nodes_after = []
                    for dep in graph_data[w]["deps"]:
                        if "tree_pos" in graph_data[w]:
                            if int(dep) < int(w):
                                nodes_before.append(int(dep))
                            elif int(dep) > int(w):
                                nodes_after.append(int(dep))
                    
                    s_nodes_before = sorted(nodes_before)
                    s_nodes_after = sorted(nodes_after)
                    
                    line_key = ""
                    if "tree_pos" not in graph_data[w]:
                        line_key += ">"
                    else:
                        line_key += graph_data[w]["tree_pos"] + ">"
                    
                    for n in s_nodes_before:
                        n = str(n)
                        edge = graph_data[w]["deps"][n]
                        pos = graph_data[n]["tree_pos"]
                        line_key += pos + "|" + edge + "&"
                    line_key += ">"
                    
                    for n in s_nodes_after:
                        n = str(n)
                        edge = graph_data[w]["deps"][n]
                        pos = graph_data[n]["tree_pos"]
                        line_key += pos + "|" + edge + "&"
                        
                    pos_to_count[line_key] += 1
                    
                graph_data = {}
                noun_list = []
                continue
            if line != "\n":
                fields = line.split("\t")
                word_id = fields[0]
                word = fields[1]
                tree_pos = fields[3]
                ud_pos = fields[4]
                mor = fields[5]
                head = fields[6]
                ud_edge = fields[7]

                make_default_structure(graph_data, word_id)
                graph_data[word_id]["word"] = word
                graph_data[word_id]["tree_pos"] = sanitize_word(ud_pos)
                graph_data[word_id]["mor"] = mor

                make_default_structure(graph_data, head)
                graph_data[head]["deps"][word_id] = ud_edge            
                
    sorted_x = sorted(pos_to_count.items(), key=operator.itemgetter(1), reverse=True)
    sorted_dict = OrderedDict(sorted_x)
    add_unseen_rules(sorted_dict, fn_dev)
    with open("train_subgraphs", "w") as out_f:
        for pos in sorted_dict:
            w_from = pos.split(">")[0]
            w_before = pos.split(">")[1]
            w_after = pos.split(">")[2]
            out_f.write(w_from + "\t" + w_before.strip("&") + "\t" + w_after.strip("&") + "\t" + str(pos_to_count[pos]) + "\n")


def sanitize_word(word):
    for pattern, target in REPLACE_MAP.items():
        word = word.replace(pattern, target)
    for digit in "0123456789":
        word = word.replace(digit, "DIGIT")
    if word in KEYWORDS:
        word = word.upper()
    return word


def get_conll_from_file(fn):
    id_to_conll = defaultdict(dict)

    sentences = 0
    with open(fn, "r") as f:
        for line in f:
            if line == "\n":
                sentences += 1
            if line.startswith("#"):
                continue
            if line != "\n":
                fields = line.split("\t")
                word_id = fields[0]
                lemma = fields[1]
                word = fields[2]
                tree_pos = fields[3]
                ud_pos = fields[4]
                mor = fields[5]
                head = fields[6]
                ud_edge = fields[7]
                comp_edge = fields[8]
                space_after = fields[9]
                
                id_to_conll[sentences][word_id] = [lemma, word, tree_pos, ud_pos,  mor, head, ud_edge, comp_edge, space_after]

    return id_to_conll


def generate_terminal_ids(conll, grammar_fn):
    TEMPLATE = (
        '{0} -> {0}_{1}\n[string] {0}_{1}\n[ud] "({0}_{1}<root> / {0}_{1})"\n')

    for w_id in conll:
        print(TEMPLATE.format(sanitize_word(conll[w_id][3]), w_id), file=grammar_fn)


def generate_terminals(fn, grammar_fn):
    TEMPLATE = (
        '{0} -> {1}_{2}_{0}\n[string] {1}\n[ud] "({1}_{2}<root> / {1}_{2})"\n')

    with open(fn) as train_file:
        terminals = set()
        words = defaultdict(int)
        for line in train_file:
            if line.startswith("#"):
                continue
            if line.strip():
                fields = line.split("\t")
                word = sanitize_word(fields[1])
                if ENGLISH_WORD.match(word):
                    terminals.add(
                        word + "_" + str(words[word]) + "_" + fields[3])
                    words[word] += 1
            elif not line.strip():
                words = defaultdict(int)

    for terminal in terminals:
        t_field = terminal.split("_")
        print(TEMPLATE.format(t_field[2],
                              t_field[0], t_field[1]), file=grammar_fn)


def generate_grammar(fn, rules, grammar_fn):
    start_rule_set = set()
    print("interpretation string: de.up.ling.irtg.algebra.StringAlgebra",
          file=grammar_fn)
    print(
        "interpretation ud: de.up.ling.irtg.algebra.graph.GraphAlgebra",
        file=grammar_fn)
    print("\n", file=grammar_fn)

    with open(fn) as count_file:
        frequencies = [int(line.split("\t")[3]) for line in count_file]
        freq_sums = sum(frequencies)

    counter = 1
    with open(fn) as count_file:
        for line in count_file:
            counter += 1
            fields = line.split("\t")
            head = fields[0]
            dep_before = fields[1].replace(":", "_")
            dep_after = fields[2].replace(":", "_")
            frequency = fields[3]
            #dep_name = fields[2].replace(":", "_")
            if head:
                start_rule_set.add(head)
            print_rules_constraint(
                head,
                dep_before,
                dep_after,
                counter,
                int(frequency),
                freq_sums,
                rules,
                grammar_fn)

    print_start_rule(start_rule_set, grammar_fn)


def print_rules(
        h,
        d_before,
        d_after,
        counter,
        frequency,
        freq_sums,
        rules,
        grammar_fn):
    freq = frequency / freq_sums
    rewrite_rule = h + " -> rule_" + str(counter) + "(" + h + ","
    if not d_before and not d_after:
        return

    before_nodes = []
    before_edges = []
    after_nodes = []
    after_edges = []

    if d_before:
        for n in d_before.split("&"):
            n = n.split("|")
            rewrite_rule += n[0] + ","
            before_nodes.append(n[0])
            before_edges.append(n[1])

    if d_after:
        for n in d_after.split("&"):
            n = n.split("|")
            rewrite_rule += n[0] + ","
            after_nodes.append(n[0])
            after_edges.append(n[1])

    rewrite_rule = rewrite_rule.strip(",")
    rewrite_rule += ") "
    rewrite_rule += "[" + str(freq) + "]"

    print(rewrite_rule)
    generate_string_line(h, before_nodes, after_nodes, grammar_fn)
    generate_graph_line(before_edges, after_edges, grammar_fn)
    print()


def remove_bidirection(id_to_rules):
    graphs_with_dirs = {}
    id_to_direction = {}

    for ind in id_to_rules:
        for i,graph in enumerate(id_to_rules[ind]):
            dict_key = tuple(sorted(graph.items()))[1:]
            if dict_key not in graphs_with_dirs:
                graphs_with_dirs[dict_key] = (ind,i)
                id_to_direction[(ind,i)] = graph["dir"]
            else:
                graph_id = graphs_with_dirs[dict_key]
                if id_to_direction[graph_id] != graph["dir"]:
                    id_to_rules[ind][i]["dir"] = None
                    id_to_rules[graph_id[0]][graph_id[1]]["dir"] = None


def print_rules_constraint(
        h,
        d_before,
        d_after,
        counter,
        frequency,
        freq_sums,
        rules,
        grammar_fn):
    freq = frequency / freq_sums
    rewrite_rule = h + " -> rule_" + str(counter) + "(" + h + ","
    if not d_before and not d_after:
        return

    id_to_graph = {}
    id_to_edges = {}
    id_to_nodes = {}
    id_to_rules = {}
    senid = 0

    for graph in rules:
        id_to_graph[senid] = graph

        subgraph_nodes = []
        subgraph_nodes.append(graph["root"])
        subgraph_edges = []
        subgraph_rules = []

        for e in graph["graph"]:
            subgraph_nodes.append(e["to"])
            subgraph_edges.append(e["edge"])
            if e['dir']:
                subgraph_rules.append(
                        {"root": graph["root"], "to": e["to"], "dir": e["dir"], "edge": e["edge"]})

        id_to_nodes[senid] = sorted(subgraph_nodes)
        id_to_edges[senid] = sorted(subgraph_edges)
        id_to_rules[senid] = subgraph_rules
        senid += 1

    remove_bidirection(id_to_rules)

    before_nodes = []
    before_edges = []
    after_nodes = []
    after_edges = []

    if d_before:
        for n in d_before.split("&"):
            n = n.split("|")
            rewrite_rule += n[0] + ","
            before_nodes.append(n[0])
            before_edges.append(n[1])

    if d_after:
        for n in d_after.split("&"):
            n = n.split("|")
            rewrite_rule += n[0] + ","
            after_nodes.append(n[0])
            after_edges.append(n[1])


    conc_nodes = before_nodes + after_nodes
    conc_nodes.append(h)
    sorted_nodes = sorted(conc_nodes)
    sorted_edges = sorted(before_edges + after_edges)

    sorted_nodes_counter = defaultdict(int)

    for node in sorted_nodes:
        sorted_nodes_counter[node] += 1

    drop = False
    found = False
    for i in id_to_nodes:
        rule_nodes_counter = defaultdict(int)
        for elem in id_to_nodes[i]:
            rule_nodes_counter[elem] += 1

        if all(
            elem in id_to_nodes[i] for elem in sorted_nodes) and all(
            elem in id_to_edges[i] for elem in sorted_edges) and all(
                rule_nodes_counter[elem] >= sorted_nodes_counter[elem] for elem in sorted_nodes):

            # if id_to_nodes[i] == sorted_nodes and id_to_edges[i] ==
            # sorted_edges:
            found = True
            for rule in id_to_rules[i]:
                if rule["dir"] == "B":
                    for ind, n in enumerate(after_nodes):
                        if n == rule["to"] and h == rule['root'] and after_edges[ind] == rule['edge']:
                            drop = True
                if rule["dir"] == "S":
                     for ind, n in enumerate(before_nodes):
                        if n == rule["to"] and h == rule['root'] and before_edges[ind] == rule['edge']:
                            drop = True
    if not found and rules:
        return
    if drop and rules:
        return

    rewrite_rule = rewrite_rule.strip(",")
    rewrite_rule += ") "
    rewrite_rule += "[" + str(freq) + "]"

    print(rewrite_rule, file=grammar_fn)
    generate_string_line(h, before_nodes, after_nodes, grammar_fn)
    generate_graph_line(before_edges, after_edges, grammar_fn)
    print(file=grammar_fn)


def generate_string_line(h, before_nodes, after_nodes, grammar_fn):
    string_temp = '[string] *({0})'
    nodes = []
    for i, node in enumerate(before_nodes):
        nodes.append("?" + str(i + 2))

    nodes.append("?1")

    for i, node in enumerate(after_nodes):
        nodes.append("?" + str(i + len(before_nodes) + 2))

    pairs = copy.deepcopy(nodes)

    while len(pairs) != 2:
        copy_pairs = []
        if len(pairs) % 2 == 0:
            for n in range(1, len(pairs), 2):
                copy_pairs.append(
                    "*(" + str(pairs[n - 1]) + "," + str(pairs[n]) + ")")
        elif len(pairs) % 2 == 1:
            for n in range(1, len(pairs), 2):
                copy_pairs.append(
                    "*(" + str(pairs[n - 1]) + "," + str(pairs[n]) + ")")
            copy_pairs.append(pairs[-1])

        pairs = copy_pairs

    string_line = string_temp.format(pairs[0] + "," + pairs[1])

    print(string_line, file=grammar_fn)


def generate_graph_line(before_edges, after_edges, grammar_fn):
    graph_line = "[ud] "
    edges = before_edges + after_edges

    if not edges:
        return
    for i in reversed(range(len(edges))):
        graph_line += "f_dep" + str(i + 1) + "("
    for i in range(len(edges)):
        graph_line += "merge("
    graph_line += "merge("
    graph_line += '?1,"(r<root> '

    for i, edge in enumerate(edges):
        graph_line += ":" + edge + " " + \
            "(d" + str(i + 1) + "<dep" + str(i + 1) + ">) "
    graph_line = graph_line.strip()
    graph_line += ')"), '

    for i, edge in enumerate(edges):
        graph_line += "r_dep" + str(i + 1) + "(?" + str(i + 2) + ")), "
    graph_line = graph_line.strip().strip(",")

    for i in range(len(edges)):
        graph_line += ")"
    print(graph_line, file=grammar_fn)


def print_start_rule(s, grammar_fn):
    for i in s:
        print("S! -> start_b_{}({}) [1.0]".format(i, i), file=grammar_fn)
        print("[string] ?1", file=grammar_fn)
        print("[ud] ?1", file=grammar_fn)
        print(file=grammar_fn)
