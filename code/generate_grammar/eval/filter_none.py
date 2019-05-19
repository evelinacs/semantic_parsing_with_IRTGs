import sys

def main(tree_in_fn, tree_out_fn, dep_in_fn, dep_out_fn):
    with open(tree_in_fn) as tree_in, open(tree_out_fn, 'w') as tree_out, open(dep_in_fn) as dep_in, open(dep_out_fn, 'w') as dep_out:
        for tree_line, dep_line in zip(tree_in, dep_in):
            if '<none>\n' == dep_line:
                continue

            print(tree_line, end='', file=tree_out)
            print(dep_line, end='', file=dep_out)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])