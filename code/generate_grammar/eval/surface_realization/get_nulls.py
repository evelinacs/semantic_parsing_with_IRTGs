import sys

def get_nulls(fn1, fn2):
    with open(fn1) as alto_input:
        with open(fn2) as alto_output:
            for line in alto_input:
                if line.startswith("#"):
                    continue
                if alto_output.readline() == "null\n":
                    print(line, end="")
                alto_output.readline()

get_nulls(sys.argv[1], sys.argv[2])