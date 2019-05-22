import sys

def get_uniq(fn):
    seen = []
    with open(fn) as input_graphs:
        for line in input_graphs:
            if line not in seen:
                print(line, end='')
                seen.append(line)
            else:
                continue

get_uniq(sys.argv[1])
