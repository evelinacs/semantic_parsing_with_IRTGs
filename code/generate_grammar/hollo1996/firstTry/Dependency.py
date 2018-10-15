from Fourlang import Fourlang
from Short2Long import *
from Digiter import *


class Dependency:
    dependencyToFourlang = {}

    def __init__(self, depType, startWord, endWord):
        if len(self.dependencyToFourlang) == 0:
            Dependency.dependencyToFourlang["advcl"] = Fourlang.ZeroTo
            Dependency.dependencyToFourlang["advmod"] = Fourlang.ZeroTo
            Dependency.dependencyToFourlang["amod"] = Fourlang.ZeroTo
            Dependency.dependencyToFourlang["nmod"] = Fourlang.ZeroTo
            Dependency.dependencyToFourlang["nummod"] = Fourlang.ZeroTo
            Dependency.dependencyToFourlang["dep"] = Fourlang.UnderTo
            Dependency.dependencyToFourlang["neg"] = Fourlang.UnderTo
            Dependency.dependencyToFourlang["appos"] = Fourlang.Zero
            Dependency.dependencyToFourlang["dislocated"] = Fourlang.Zero
            Dependency.dependencyToFourlang["csubj"] = Fourlang.OneTo_ZeroBack
            Dependency.dependencyToFourlang["nsubj"] = Fourlang.OneTo_ZeroBack
            Dependency.dependencyToFourlang["ccomp"] = Fourlang.TwoTo
            Dependency.dependencyToFourlang["obj"] = Fourlang.TwoTo
            Dependency.dependencyToFourlang["xcomp"] = Fourlang.TwoTo
            Dependency.dependencyToFourlang["case"] = Fourlang.OneBack__TwoTo
            Dependency.dependencyToFourlang["caseNmod"] = Fourlang.OneBack__TwoTo
            Dependency.dependencyToFourlang["caseNsubj"] = Fourlang.OneBack__TwoTo
            Dependency.dependencyToFourlang["caseNobl"] = Fourlang.OneBack__TwoTo
            Dependency.dependencyToFourlang["obl:npmod"] = Fourlang.ZeroTo
            Dependency.dependencyToFourlang["nmod:tmod "] = Fourlang.OneBack_at_TwoTo
            Dependency.dependencyToFourlang["obl:tmod"] = Fourlang.OneBack_has_TwoTo
            Dependency.dependencyToFourlang["nmod:poss"] = Fourlang.OneBack_has_TwoTo
            Dependency.dependencyToFourlang["compound"] = Fourlang.ZeroCompound
            Dependency.dependencyToFourlang["flat"] = Fourlang.ZeroFlat
            Dependency.dependencyToFourlang["root"] = Fourlang._None
            Dependency.dependencyToFourlang["det"] = Fourlang._None
            Dependency.dependencyToFourlang["det:predet"] = Fourlang._None
            Dependency.dependencyToFourlang["cc"] = Fourlang.UnderTo
            Dependency.dependencyToFourlang["conj:&"] = Fourlang.UnderTo
            Dependency.dependencyToFourlang["conj:and"] = Fourlang.UnderTo
            Dependency.dependencyToFourlang["conj:v."] = Fourlang.UnderTo
            Dependency.dependencyToFourlang["conj:or"] = Fourlang.UnderTo

        self.depType = depType
        self.startWord = startWord
        self.endWord = endWord
        self.flangType = self.dependencyToFourlang[Short2Long.getShortest(depType)]

    # [nummod(%-2, 0.05-1), root(ROOT-0, %-2)]
    @staticmethod
    def fromString(terminal):
        terminal = str(terminal)

        dataParts = terminal[1:len(terminal) - 3].split("), ")
        result = []
        tmp = []
        tmptmp = []

        for i in range(0, len(dataParts)):
            dataParts[i] = dataParts[i][0:len(dataParts[i])].replace("(", "#", 1).replace(", ", "#", 1)
            tmp = dataParts[i].split("#")

            tmptmp = tmp[1].split("-")
            tmp[1] = ""
            for j in range(0, len(tmptmp) - 1):
                tmp[1] += tmptmp[j]
                if (j != len(tmptmp) - 2):
                    tmp[1] += "-"

            tmptmp = tmp[2].split("-")
            tmp[2] = ""
            for j in range(0, len(tmptmp) - 1):
                tmp[2] += tmptmp[j]
                if (j != len(tmptmp) - 2):
                    tmp[2] += "-"

            tmp[1]=Digiter.toDigited(tmp[1])
            tmp[2]=Digiter.toDigited(tmp[2])

            if tmp[0] == "neg":
                tmp[0] = "det"
            result.insert(0, Dependency(Short2Long.dependency[tmp[0]], tmp[1], tmp[2]))

        return result
