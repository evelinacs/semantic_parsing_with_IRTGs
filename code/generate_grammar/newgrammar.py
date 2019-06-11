import sys

def generate_grammar(fn):
    start_rule_set = set()
    print("interpretation string: de.up.ling.irtg.algebra.StringAlgebra")
    print("interpretation ud: de.up.ling.irtg.algebra.graph.GraphAlgebra")
    print("\n")
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

            start_rule_set.add(head)
            print_rules(head, dep_before, dep_after, counter)

    print_start_rule(start_rule_set)


def print_rules(h, d_before, d_after, counter):
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
    rewrite_rule += ")"

    print(rewrite_rule)
    generate_string_line(h, before_nodes, after_nodes)
    generate_graph_line(before_edges, after_edges)

    #print("{} -> {}_{}_{}({}, {})".format(h, h, d, n, d, h))
    #print("[string] *(?1,?2)")
    #print('[ud] merge(f_dep(merge("(r<root> :{} (d<dep>))", r_dep(?1))),?2)'.format(n))
    #print("\n")

#f_dep2(f_dep1(merge(merge(merge(?1,"(r<root> :compound (d1<dep1>) :punct (d2<dep2>))"), r_dep1(?2)), r_dep2(?3))))

def generate_string_line(h, before_nodes, after_nodes):
    string_line = "[string] *("
    for i, node in enumerate(before_nodes):
        string_line += "?" + str(i+2) + ","

    string_line += "?1" + ","

    for i, node in enumerate(after_nodes):
        string_line += "?" + str(i+len(before_nodes)+2) + ","
    string_line = string_line.strip(",")
    string_line += ")"

    print(string_line)


def generate_graph_line(before_edges, after_edges):
    graph_line = "[ud] "
    edges = before_edges + after_edges
    
    if not edges:
        return
    for i in range(len(edges)):
        graph_line += "f_dep" + str(i) + "("
        graph_line += "merge("
    graph_line += "merge("
    graph_line += '?1,"(r<root> '
    
    for i, edge in enumerate(edges):
        graph_line += ":" + edge + " " + "(d" + str(i+1) + "<dep" + str(i+1) + ">) "
    graph_line = graph_line.strip()
    graph_line += ')"), '
    
    for i, edge in enumerate(edges):
        graph_line += "r_dep" + str(i+1) + "(?" + str(i+2) + ")), "
    graph_line = graph_line.strip().strip(",")
    
    for i in range(len(edges)):
        graph_line += ")"
    print(graph_line)
    
def print_start_rule(s):
    for i in s:
        print("S! -> start_{}({})".format(i, i))
        print("[string] ?1")
        print("[ud] ?1")
        print("\n")


generate_grammar(sys.argv[1])