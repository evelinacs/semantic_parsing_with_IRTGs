import sys
import argparse
import re

SEEN = set()

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
    parser.add_argument("-t", "--terminals", action = "store_true", help = "generate Penn Treebank terminal nodes")
    parser.add_argument("-u", "--ud_terminals", action = "store_true", help = "generate UD terminal nodes")
    return parser.parse_args()


def make_default_structure(graph_data, word_id):
    if word_id not in graph_data:
        graph_data[word_id] = {
            "word": "",
            "deps": {},
        }


def print_output(graph_data, graph_root, args):
    if args.terminals or args.ud_terminals:
        print_all_terminals(graph_data, graph_root, args)
    else:
        print(make_graph_string(graph_data, graph_root))


def make_graph_string(graph_data, word_id):
    graph_string = "({0} / {0}".format(graph_data[word_id]["word"])
    for other_id in graph_data[word_id]["deps"]:
        edge = graph_data[word_id]["deps"][other_id]
        graph_string += ' :{0} '.format(edge.replace(':', '_'))
        graph_string += make_graph_string(graph_data, other_id)
    graph_string += ")"
    return graph_string


def print_terminal(graph_data, word_id, args):
    word = graph_data[word_id]["word"]
    if args.ud_terminals:
        pos = graph_data[word_id]["ud_pos"]
    if args.terminals:
        pos = graph_data[word_id]["tree_pos"]

    signature = '{}_{}'.format(word, pos)
    if signature not in SEEN:
        SEEN.add(signature)
        print(TEMPLATE.format(pos, word))


def print_all_terminals(graph_data, word_id, args):
    print_terminal(graph_data, word_id, args)
    for other_id in  graph_data[word_id]["deps"]:
        print_all_terminals(graph_data, other_id, args)


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


def main():
    args = get_args()
    if not args.terminals and not args.ud_terminals:
        print("# IRTG unannotated corpus file, v1.0")
        print("# interpretation ud: de.up.ling.irtg.algebra.graph.GraphAlgebra")

    with open(args.conll_file) as conll_file:
        graph_data = {}
        graph_root = "0"
        for line in conll_file:
            if line == "\n":
                print_output(graph_data, graph_root, args)
                graph_data = {}
                graph_root = "0"
                continue

            fields = line.split("\t")
            dep_word_id = fields[0]
            dep_word = sanitize_word(fields[1])
            tree_pos = sanitize_word(sanitize_pos(fields[4]))
            ud_pos = fields[3]
            root_word_id = fields[6]
            ud_edge = fields[7]

            make_default_structure(graph_data, dep_word_id)
            graph_data[dep_word_id]["word"] = dep_word
            graph_data[dep_word_id]["tree_pos"] = tree_pos
            graph_data[dep_word_id]["ud_pos"] = ud_pos

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
