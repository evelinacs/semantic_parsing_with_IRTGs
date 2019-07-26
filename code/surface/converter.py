import sys
import argparse
import re
from collections import defaultdict

SEEN = set()

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
NON_ENGLISH_CHARACTERS = re.compile(r"[^a-zA-Z]")

KEYWORDS = set(["feature"])

TEMPLATE = (
    '{0} -> {1}_{0}\n' +
    '[string] {1}\n' +
    '[tree] {0}({1})\n' +
    '[ud] "({1}<root> / {1})"\n' +
    '[fourlang] "({1}<root> / {1})"\n'
)


def sanitize_word(word):
    for pattern, target in REPLACE_MAP.items():
        word = word.replace(pattern, target)
    for digit in "0123456789":
        word = word.replace(digit, "DIGIT")
    if word in KEYWORDS:
        word = word.upper()
    NON_ENGLISH_CHARACTERS.sub("SPECIALCHAR", word)

    return word

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


def extract_rules(dev):
    graph_data = {}
    noun_list = []
    id_to_rules = defaultdict(list)
    id_to_sentence = {}
    sentences = 0
    with open(dev, "r") as f:
        for i,line in enumerate(f):            
            if line == "\n":
                words = []
                for w in graph_data:
                    words.append(graph_data[w]["word"])
                    subgraphs = {"root": None, "graph": []}
                    rules = []
                    if "tree_pos" not in graph_data[w]:
                        continue
                    
                    subgraphs["root"] = graph_data[w]["tree_pos"]
                    
                    for dep in graph_data[w]["deps"]:                        
                        edge_dep = graph_data[w]["deps"][dep]
                        to_pos = graph_data[dep]["tree_pos"]
                        mor = graph_data[dep]["mor"]
                            
                        if "tree_pos" in graph_data[w]:
                            if "lin=+" in mor:
                                subgraphs["graph"].append({"to":to_pos, "edge":edge_dep.replace(":", "_"), "dir":"S"})
                            elif "lin=-" in mor:
                                subgraphs["graph"].append({"to":to_pos, "edge":edge_dep.replace(":", "_"), "dir":"B"})
                            else:
                                subgraphs["graph"].append({"to":to_pos, "edge":edge_dep.replace(":", "_"), "dir":None})

                    id_to_rules[sentences].append(subgraphs)
                graph_data = {}
                noun_list = []
                sentences += 1
                continue
            if line.startswith("# text"):
                id_to_sentence[sentences] = line.strip()
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
                
                make_default_structure(graph_data, word_id)
                graph_data[word_id]["word"] = lemma
                graph_data[word_id]["tree_pos"] = sanitize_word(ud_pos)
                graph_data[word_id]["mor"] = mor

                make_default_structure(graph_data, head)
                graph_data[head]["deps"][word_id] = ud_edge
    return id_to_rules, id_to_sentence


def print_output(graph_data, graph_root):
    print(make_graph_string(graph_data, graph_root))


def make_id_graph(graph_data, word_id):
    graph_string = "({1}_{0} / {1}_{0}".format(str(word_id), graph_data[word_id]["ud_pos"])
    for other_id in graph_data[word_id]["deps"]:
        edge = graph_data[word_id]["deps"][other_id]
        graph_string += ' :{0} '.format(edge.replace(':', '_'))
        graph_string += make_id_graph(graph_data, other_id)
    graph_string += ")"
    return graph_string


def make_graph_string(graph_data, word_id):
    graph_string = "({0} / {0}".format(graph_data[word_id]["word"])
    for other_id in graph_data[word_id]["deps"]:
        edge = graph_data[word_id]["deps"][other_id]
        graph_string += ' :{0} '.format(edge.replace(':', '_'))
        graph_string += make_graph_string(graph_data, other_id)
    graph_string += ")"
    return graph_string


def sanitize_pos(pos):
    if pos == "HYPH":
        pos = "PUNCT"

    pos = pos.replace("|", "PIPE")
    pos = pos.replace("=", "EQUAL")

    is_punct = True
    for character in pos:
        if character not in REPLACE_MAP:
            is_punct = False

    if is_punct == True:
        return "PUNCT"
    else:
        return pos


def convert(conll_file):
    sentences = []
    graphs = []
    words = defaultdict(int)
    id_to_sentences = {}
    id_to_graph = {}
    id_to_idgraph = {}
    with open(conll_file) as conll_file:
        graph_data = {}
        graph_root = "0"
        sen_id = 0
        for line in conll_file:
            if line == "\n":
                graph = make_graph_string(graph_data, graph_root)
                id_graph = make_id_graph(graph_data, graph_root)
                graphs.append(graph)
                id_to_graph[sen_id] = graph
                id_to_idgraph[sen_id] = id_graph
                graph_data = {}
                graph_root = "0"
                words = defaultdict(int)
                sen_id += 1
                continue
            if line.startswith("# text ="):
                sentence = line.split("=")[1]
                graphs.append(line.strip())
                id_to_sentences[sen_id] = line.strip()
                continue
            elif line.startswith("#") or not line:
                continue

            fields = line.split("\t")
            dep_word_id = fields[0]

            dep_word = sanitize_word(fields[1])
            dep_word_unique = dep_word + "_" + str(words[dep_word])
            words[dep_word] += 1

            tree_pos = sanitize_word(sanitize_pos(fields[3]))
            ud_pos = fields[4]
            root_word_id = fields[6]
            ud_edge = fields[7]

            make_default_structure(graph_data, dep_word_id)
            graph_data[dep_word_id]["word"] = dep_word_unique
            graph_data[dep_word_id]["tree_pos"] = tree_pos
            graph_data[dep_word_id]["ud_pos"] = sanitize_word(ud_pos)

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

    with open("ewt_graphs", "w") as f:
        f.write("# IRTG unannotated corpus file, v1.0\n")
        f.write("# interpretation ud: de.up.ling.irtg.algebra.graph.GraphAlgebra\n")
        for graph in graphs:
            f.write(graph + "\n")
    with open("ewt_sentences", "w") as f:
        for sentence in sentences:
            f.write(sentence + "\n")

    return id_to_graph, id_to_sentences, id_to_idgraph


def main():
    args = get_args()
    convert(args.conll_file)


if __name__ == "__main__":
    main()
