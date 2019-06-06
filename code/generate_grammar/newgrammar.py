import sys

def generate_grammar(fn):
    start_rule_set = set()
    print("interpretation string: de.up.ling.irtg.algebra.StringAlgebra")
    print("interpretation ud: de.up.ling.irtg.algebra.graph.GraphAlgebra")
    print("\n")
    with open(fn) as count_file:
        for line in count_file:
            fields = line.split("\t")
            head = fields[0]
            dependent = fields[1]
            dep_name = fields[2].replace(":", "_")

            start_rule_set.add(head)
            print_rules(head, dependent, dep_name)

    print_start_rule(start_rule_set)




def print_rules(h, d, n):
    print("{} -> {}_{}_{}({}, {})".format(h, h, d, n, d, h))
    if n == "obj":
        print("[string] *(?2,?1)")
    else:
        print("[string] *(?1,?2)")
    print('[ud] merge(f_dep(merge("(r<root> :{} (d<dep>))", r_dep(?1))),?2)'.format(n))
    print("\n")


def print_start_rule(s):
    for i in s:
        print("S! -> start_{}({})".format(i, i))
        print("[string] ?1")
        print("[ud] ?1")
        print("\n")


generate_grammar(sys.argv[1])