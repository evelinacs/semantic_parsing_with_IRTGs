import sys

from nltk.tree import Tree


with open(sys.argv[1]) as tree_file:
	for line in tree_file:
		l = Tree.fromstring(line)
		print(l.pos())


