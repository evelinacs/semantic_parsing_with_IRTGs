import argparse

from utils import sanitize_word


def get_args():
    parser = argparse.ArgumentParser(description = "Create unannotated corpus for Alto, containing string and UD data")
    parser.add_argument("conll_file", type = str, help = "path to the CoNLL file")
    parser.add_argument("-t", "--tree", required = True, choices = ['np', 'sen'], help = "extract full sentences or NPs")
    return parser.parse_args()


def make_default_structure(graph_data, word_id):
    if word_id not in graph_data:
        graph_data[word_id] = {
            "word": "",
            "deps": {},
        }


def conll_reader(conll_file):
    graph_data = {}
    noun_list = []

    for line in conll_file:
        if line.startswith("#"):
            continue

        if line == "\n":
            yield graph_data, noun_list
            graph_data = {}
            noun_list = []
            continue

        fields = line.split("\t")
        word_id = int(fields[0])
        word = sanitize_word(fields[1])
        tree_pos = fields[4]
        head = int(fields[6])
        ud_edge = fields[7]

        make_default_structure(graph_data, word_id)
        graph_data[word_id]["word"] = word

        """
        for the head; store the edges with the head of the dependency
        """
        if ud_edge == "root":
            graph_data["root"] = word_id
        else:
            make_default_structure(graph_data, head)
            graph_data[head]["deps"][word_id] = ud_edge
        
        if tree_pos in ["NN", "NNS", "NNP", "NNPS"]:
            noun_list.append(word_id)


def print_corpus_header():
    print("/// IRTG unannotated corpus file, v1.0")
    print("///")
    print("/// interpretation string: de.up.ling.irtg.algebra.StringAlgebra")
    print("/// interpretation ud: de.up.ling.irtg.algebra.graph.GraphAlgebra")
    print()


def print_corpus_data(text, isi):
    print(text)
    print(isi)
    print()


def process_sentence(graph_data):
    word_id_list = []
    isi = get_graph_isi(graph_data, graph_data["root"], word_id_list)
    text = get_graph_text(graph_data, word_id_list)
    print_corpus_data(text, isi)


def process_nps(graph_data, noun_list):
    for noun_id in noun_list:
        word_id_list = []
        isi = get_graph_isi(graph_data, noun_id, word_id_list, exclude_from_np)
        text = get_graph_text(graph_data, word_id_list)
        print_corpus_data(text, isi)


def exclude_from_np(edge):
    exclude_list = ["case", "cc"]
    if edge in exclude_list:
        return True
    else:
        return False


def get_graph_isi(graph_data, word_id, word_id_list, graph_filter = None):
    word_id_list.append(word_id)
    graph_string = "({0} / {0}".format(graph_data[word_id]["word"])
    for other_id in graph_data[word_id]["deps"]:
        edge = graph_data[word_id]["deps"][other_id]
        if graph_filter is not None and graph_filter(edge):
            continue

        graph_string += ' :{0} '.format(edge.replace(':', '_'))
        graph_string += get_graph_isi(graph_data, other_id, word_id_list, graph_filter)
    graph_string += ")"
    return graph_string


def get_graph_text(graph_data, id_list):
    text_list = []
    id_list = sorted(id_list)
    for word_id in id_list:
        text_list.append(graph_data[word_id]["word"])
    return " ".join(text_list)


def main():
    args = get_args()
    print_corpus_header()
    with open(args.conll_file) as conll_file:
        for graph_data, noun_list in conll_reader(conll_file):
            if args.tree == "np":
                process_nps(graph_data, noun_list)
            elif args.tree == "sen":
                process_sentence(graph_data)


if __name__ == "__main__":
    main()