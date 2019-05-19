import sys
import argparse

from utils import sanitize_word

SEEN = set()


def get_args():
    parser = argparse.ArgumentParser(description = "Convert conllu file to isi file")
    parser.add_argument("conll_file", type = str, help = "path to the CoNLL file")
    return parser.parse_args()


def make_default_structure(graph_data, word_id):
    if word_id not in graph_data:
        graph_data[word_id] = {
            "word": "",
            "deps": {},
        }


def print_output(graph_data, graph_root):
    print(make_graph_string(graph_data, graph_root))


def make_graph_string(graph_data, word_id):
    graph_string = "({0} / {0}-{1}".format(graph_data[word_id]["word"], word_id)
    for other_id in graph_data[word_id]["deps"]:
        edge = graph_data[word_id]["deps"][other_id]
        graph_string += ' :{0} '.format(edge.replace(':', '_'))
        graph_string += make_graph_string(graph_data, other_id)
    graph_string += ")"
    return graph_string


def main():
    args = get_args()
    with open(args.conll_file) as conll_file:
        graph_data = {}
        graph_root = "0"
        for line in conll_file:
            if line == "\n":
                print_output(graph_data, graph_root)
                graph_data = {}
                graph_root = "0"
                continue

            fields = line.split("\t")
            dep_word_id = fields[0]
            dep_word = sanitize_word(fields[1])
            root_word_id = fields[6]
            ud_edge = fields[7]

            make_default_structure(graph_data, dep_word_id)
            graph_data[dep_word_id]["word"] = dep_word

            """
            for the head; store the edges with the head of the dependency
            """
            # Ignore :root dependencies,
            # but remember the root word of the graph
            if "0" != root_word_id:
                make_default_structure(graph_data, root_word_id)
                graph_data[root_word_id]["deps"][dep_word_id] = ud_edge
            else:
                graph_root = dep_word_id


if __name__ == "__main__":
    main()
