import sys
import re

def get_derivation_trees(fn):
    derivations = []
    with open(fn) as parse_output:
        for line in parse_output:
            if line.startswith("sentence"):
                derivations.append(line)
        return derivations


def get_rules(derivations):
    rule_list = []
    for tree in derivations:
        tree = tree.replace("(", "\n")
        tree = tree.replace(",", "\n")
        tree = tree.replace(")", "")
        rule_list.append(tree)
    return rule_list


def count_rules(rule_list):
    rule_dict = {}
    for i in rule_list:
        i = i.split("\n")
        for rule in i:
            if rule == "":
                continue
            if rule in rule_dict:
                rule_dict[rule] += 1
            else: 
                rule_dict[rule] = 1
    return rule_dict


def extract_irtg_rule(fn):
    irtg_rule_list = []
    with open(fn) as irtg:
        for line in irtg:
            if line.startswith("interpretation"):
                continue
            if line == "\n":
                continue
            if line.startswith("["):
                continue
            if line.startswith("/"):
                continue
            irtg_rule_list.append(line)
        return irtg_rule_list


def get_irtg_rule_name(irtg_rule_list):
    rules = []
    name_re = re.compile(r"-> +([^\(]+)(\(|\n)")
    for i in irtg_rule_list:
        name_match = name_re.search(i)
        if name_match is None:
            print('? <{}>'.format(i))
            continue
        rule_name = name_match.group(1)
        rules.append(rule_name)
    return rules


def get_missing_rules(irtg_rules, derivation_rules):
    for i in irtg_rules:
        if i not in derivation_rules:
            print(i)          


def main():
    derivation_rules = count_rules(get_rules(get_derivation_trees(sys.argv[1])))
    get_missing_rules(get_irtg_rule_name(extract_irtg_rule(sys.argv[2])), derivation_rules)

if __name__ == "__main__":
    main()
