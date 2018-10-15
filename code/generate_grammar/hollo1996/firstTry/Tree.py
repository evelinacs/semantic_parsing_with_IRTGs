from Digiter import *


class Tree:
    def __init__(self, stanford, tagTree, wordLess, words):
        self.stanford = stanford
        self.tagTree = tagTree
        self.wordLess = wordLess
        self.words = []
        self.words.extend(words)

    @classmethod
    def fromString(cls, stanIn):
        stan = str(stanIn).replace("\n","")

        result = Tree(stan, "", "", [])

        closingCount = -1

        parts = stan.split(" ")
        for i in range(0, len(parts)):
            part = parts[i]
            if part.startswith("("):
                part = Digiter.toPuncted(Digiter.toDigited(part[1:len(part)]))+"("
                result.tagTree += part
                result.wordLess += part
            elif part.endswith(")"):
                closingCount = 0

                for j in range(len(part)-1, 0, -1):
                    if part[j] == ")":
                        closingCount += 1
                    else:
                        break;

                part = Digiter.toDigited(part[0:len(part) - closingCount])
                result.words.extend([part])
                result.tagTree += part

                for j in range(0, closingCount):
                    result.tagTree += ')'
                    result.wordLess += ')'

                if i != len(parts) - 1:
                    result.tagTree += ','
                    result.wordLess += ','

            if i != len(parts) - 1:
                result.tagTree += " "
                result.wordLess += " "
        return result
