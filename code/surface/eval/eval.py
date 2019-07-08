import sys
import json


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
    for symbol in ",?.!-:":
        word = word.replace(symbol, " " + symbol + " ").replace("  ", " ")
    for pattern, target in REPLACE_MAP.items():
        word = word.replace(pattern, target)
    for digit in "0123456789":
        word = word.replace(digit, "DIGIT")

    if word in KEYWORDS:
        word = word.upper()
    return word


def main(fn):
    correct_parses = 0
    with open(fn) as parse_output:
        for line in parse_output:
            if line.startswith("#"):
                text_line = sanitize_word(line[9:]).strip()

            if line.startswith("["):
                line = " ".join(json.loads(line.replace("'", '"')))
                if line == text_line:
                    correct_parses += 1
                else:
                    print(text_line)
                    print(line)
    print(correct_parses)

main(sys.argv[1])