import sys
import argparse

from utils import sanitize_word
from utils import REPLACE_MAP

SEEN = set()
TEMPLATE = (
    '{0} -> {1}_{0}\n' +
    '[string] {1}\n' +
    '[tree] {0}({1})\n' +
    '[ud] "({1}<root> / {1})"\n' +
    '[fourlang] "({1}<root> / {1})"\n'
)


def get_args():
    parser = argparse.ArgumentParser(description = "Extract NPs/PPs from CoNLL files and respective IRTG terminals")
    parser.add_argument("conll_file", type = str, help = "path to the CoNLL file")
    parser.add_argument("-s", "--strict", action = "store_true", help = "extract only NPs")
    parser.add_argument("-t", "--terminals", action = "store_true", help = "generate terminal nodes")
    return parser.parse_args()


def print_terminal(graph_data, word_id):
    word = graph_data[word_id]["word"]
    tree_pos = graph_data[word_id]["tree_pos"]

    signature = '{}_{}'.format(word, tree_pos)
    if signature not in SEEN:
        SEEN.add(signature)
        print(TEMPLATE.format(tree_pos, word))


def print_all_terminals(graph_data, word_id):
    print_terminal(graph_data, word_id)
    for other_id in  graph_data[word_id]["deps"]:
        print_all_terminals(graph_data, other_id)


def make_default_structure(graph_data, word_id):
    if word_id not in graph_data:
        graph_data[word_id] = {
            "word": "",
            "deps": {},
        }


def print_output(graph_data, noun_list, args):
    for noun_id in noun_list:
        if args.terminals:
            print_all_terminals(graph_data, noun_id)
        else:
            print(make_graph_string(graph_data, noun_id, args))


def make_graph_string(graph_data, word_id, args):
    graph_string = "({0} / {0}".format(graph_data[word_id]["word"])
    for other_id in graph_data[word_id]["deps"]:
        edge = graph_data[word_id]["deps"][other_id]
        if exclude_edge(args, edge):
            continue

        graph_string += ' :{0} '.format(edge.replace(':', '_'))
        graph_string += make_graph_string(graph_data, other_id, args)
    graph_string += ")"
    return graph_string


def sanitize_pos(pos):
    if pos == "HYPH":
        pos = "PUNCT"
        
    is_punct = True
    for character in pos:
        if character not in REPLACE_MAP:
            is_punct = False
    
    if is_punct == True:
        return "PUNCT"
    else:
        return pos


def exclude_edge(args, edge):
    exclude_list = ["case", "cc"]
    if args.strict and edge in exclude_list:
        return True
    else:
        return False


def main():
    args = get_args()
    with open(args.conll_file) as conll_file:
        graph_data = {}
        noun_list = []
        for line in conll_file:
            if line.startswith("#"):
                continue
            if line == "\n":
                print_output(graph_data, noun_list, args)
                graph_data = {}
                noun_list = []
                continue

            fields = line.split("\t")
            word_id = fields[0]
            word = sanitize_word(fields[1])
            tree_pos = sanitize_pos(fields[4])
            head = fields[6]
            ud_edge = fields[7]

            make_default_structure(graph_data, word_id)
            graph_data[word_id]["word"] = word
            graph_data[word_id]["tree_pos"] = tree_pos  # for terminals

            """
            for the head; store the edges with the head of the dependency
            """
            make_default_structure(graph_data, head)
            graph_data[head]["deps"][word_id] = ud_edge
            
            if tree_pos in ["NN", "NNS", "NNP", "NNPS"]:
                noun_list.append(word_id)


if __name__ == "__main__":
    main()
