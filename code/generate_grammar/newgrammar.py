import sys
import re
import copy

ENGLISH_WORD = re.compile("^[a-zA-Z0-9]*$")

REPLACE_MAP = {
    ":": "COLON",
    ",": "COMMA",
    ".": "PERIOD",
    ";": "SEMICOLON",
    "-": "HYPHEN",
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


def sanitize_word(word):
    for pattern, target in REPLACE_MAP.items():
        word = word.replace(pattern, target)
    for digit in "0123456789":
        word = word.replace(digit, "DIGIT")
    if word in KEYWORDS:
        word = word.upper()
    return word


def generate_terminals(fn):
    TEMPLATE = ('{0} -> {1}_{0}\n[string] {1}\n[ud] "({1}<root> / {1})"\n')

    with open(fn) as train_file:
        terminals = set()
        for line in train_file:
            if line.strip():
                fields = line.split("\t")
                word = sanitize_word(fields[1])
                if ENGLISH_WORD.match(word):
                    terminals.add(word + "_" + fields[3])
    
    for terminal in terminals:
        t_field = terminal.split("_")
        print(TEMPLATE.format(t_field[1], t_field[0]))
    

def generate_grammar(fn):
    start_rule_set = set()
    print("interpretation string: de.up.ling.irtg.algebra.StringAlgebra")
    print("interpretation ud: de.up.ling.irtg.algebra.graph.GraphAlgebra")
    print("\n")
    
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
            print_rules(head, dep_before, dep_after, counter, int(frequency)/freq_sums)

    print_start_rule(start_rule_set)


def print_rules(h, d_before, d_after, counter, freq):
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
    generate_string_line(h, before_nodes, after_nodes)
    generate_graph_line(before_edges, after_edges)
    print()
    #print("{} -> {}_{}_{}({}, {})".format(h, h, d, n, d, h))
    #print("[string] *(?1,?2)")
    #print('[ud] merge(f_dep(merge("(r<root> :{} (d<dep>))", r_dep(?1))),?2)'.format(n))
    # print("\n")s

# f_dep2(f_dep1(merge(merge(merge(?1,"(r<root> :compound (d1<dep1>) :punct (d2<dep2>))"), r_dep1(?2)), r_dep2(?3))))


def generate_string_line(h, before_nodes, after_nodes):
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
                copy_pairs.append("*(" + str(pairs[n-1]) + "," + str(pairs[n]) + ")")
        elif len(pairs) % 2 == 1:
            for n in range(1, len(pairs), 2):
                copy_pairs.append("*(" + str(pairs[n-1]) + "," + str(pairs[n]) + ")")
            copy_pairs.append(nodes[-1])
            
        pairs = copy_pairs
        
    string_line = string_temp.format(pairs[0] + "," + pairs[1])
        
    print(string_line)


def generate_graph_line(before_edges, after_edges):
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
        graph_line += ":" + edge + " " + "(d" + str(i + 1) + "<dep" + str(i + 1) + ">) "
    graph_line = graph_line.strip()
    graph_line += ')"), '

    for i, edge in enumerate(edges):
        graph_line += "r_dep" + str(i + 1) + "(?" + str(i + 2) + ")), "
    graph_line = graph_line.strip().strip(",")

    for i in range(len(edges)):
        graph_line += ")"
    print(graph_line)


def print_start_rule(s):
    for i in s:
        print("S! -> start_b_{}({}) [1.0]".format(i, i))
        print("[string] ?1")
        print("[ud] ?1")
        print()


generate_grammar(sys.argv[1])
generate_terminals(sys.argv[2])
