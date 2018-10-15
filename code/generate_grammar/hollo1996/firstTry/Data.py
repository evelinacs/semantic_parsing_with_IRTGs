from Tree import *
from Dependency import *
from Terminal import *

"""
(NP (CD DIGITS))
    root(ROOT, DIGITDIGIT)
    [('DIGITDIGIT', 'CD')]*/
    //represents all data needed for
"""


class Data:
    def __init__(self, words, dependencies, tree):
        self.words = words
        self.dependencies = dependencies
        self.tree = tree

    """
    [nummod(%-2, 0.16-1), root(ROOT-0, %-2)]
    [('0.05', 'CD'), ('%', 'NN')]
    (NP (CD 0.05) (NN %))
    """

    @staticmethod
    def fromFile(treeLocation, termLocation, depLocation, count):
        datas = []
        words = []
        dependencies = []
        tree = Tree("", "", "", [])

        with open(treeLocation) as treeFile:
            with open(termLocation) as termFile:
                with open(depLocation) as depFile:
                    for i in range(0, count):
                        tree = Tree.fromString(treeFile.readline())

                        line=termFile.readline()
                        words = Terminal.fromString(line)

                        dependencies = Dependency.fromString(depFile.readline())

                        line = depFile.readline()
                        while line != "----------\n":
                            line = depFile.readline()
                        datas.insert(0, Data(words, dependencies, tree))
        return datas
