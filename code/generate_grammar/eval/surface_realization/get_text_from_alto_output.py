import sys

def process_alto_output(fn):
    with open(fn) as alto_output:
        for line in alto_output:
            if line.startswith("["):
                line = line[1:-2].replace(",", "")
                print(line)

process_alto_output(sys.argv[1])