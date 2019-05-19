import sys
import re

def get_bad_words_from_irtg(fn):
    bad_words = set()
    with open(fn) as grammar_file:
        for line in grammar_file:
            if line.startswith("//[string]"):
                bad_words.add(line[11:].strip()) # 11 because of an additional space
    return bad_words


def filter_corpus(fn, bad_words):
    text_line_re = re.compile(r"^[a-zA-Z]")
    filter_re = re.compile(r"\b({})\b".format("|".join(bad_words)))
    skip = 0
    with open(fn) as corpus_file:
        for line in corpus_file:
            if text_line_re.match(line):
                if filter_re.search(line):
                    skip = 3
            
            if skip > 0:
                skip -= 1
            else:
                print(line, end = "")


def main(fn1, fn2):
    bad_words = get_bad_words_from_irtg(fn1)
    filter_corpus(fn2, bad_words)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
                

