from Data import *
from Dependency import *
from Fourlang import *


"""
        //NounPhrase out of one Word
        //NP(WD(stuff))
        NP -> one_WD(WD)
        [tree] NP(?1)
        [ud] ?1
        [fourlang] ?1
"""

#This is the function that generates 2 wide, 1 high NP-s.

def basicUnariNP():
    result=""

    datas=Data.fromFile("Data/Input/NP/np_1x1_trees", "Data/Input/NP/np_1x1_terms", "Data/Input/NP/np_1x1_deps", 1642)
    uniqData={}
    for i in range(len(datas)-1,-1,-1):
        if not (uniqData.keys().__contains__(datas[i].tree.wordLess)):
            uniqData[datas[i].tree.wordLess]=datas[i]

    for input in uniqData.values():
        result+="\n"
        result+="//NounPhrase out of one " + input.words[0].type.Longer + ".\n"
        result+="//" + input.tree.stanford+"\n"
        result+="//" + input.tree.tagTree+"\n"
        result+="NP -> one_" + input.words[0].type.Shortest.replace("basic", "") + "(" + input.words[0].type.Shortest + ")\n"
        result+="[string] ?1\n"
        result+="[tree] NP(?1)\n"
        result+="[ud] ?1\n"
        result+="[fourlang] ?1\n"
    return result

"""
        //NounPhrase out of a Word1 (whitch is a Modifier1) and a Word2.
        //(NP (WD1 stuff) (WD2 stuff))
        NP -> mod1_WD1_WD2(WD1, WD2)
        [tree] NP2(?1,?2)
        [ud] merge(f_dep(merge("(r<root> :mod1 (d<dep>))", r_dep(?1))),?2)
        [fourlang] merge(f_dep(merge("(r<root> :_ (d<dep>))", r_dep(?1))),?2)
"""

#This is the function that generates 1 wide, 1 high NP-s.

def basicBinaryNP():
    reverse = False
    connected = False
    sameType = False

    result = ""
    datas = Data.fromFile("Data/Input/NP/np_1x2_trees", "Data/Input/NP/np_1x2_terms", "Data/Input/NP/np_1x2_deps", 4633)
    uniqData = {}
    for i in range(len(datas)-1,-1,-1):
        if not (uniqData.keys().__contains__(datas[i].tree.wordLess)):
            uniqData[datas[i].tree.wordLess] = datas[i]

    for input in uniqData.values():
        result+="\n"
        connected = len(input.dependencies) > 1
        sameType = input.words[0].type.Shortest == input.words[1].type.Shortest
        if connected:
            if input.dependencies[1].depType.Shortest == "root":
                input.dependencies[0], input.dependencies[1] = input.dependencies[1], input.dependencies[0]

            reverse = input.words[1].word == input.dependencies[0].endWord

            if not reverse:
                result += ("//NounPhrase out of a " + input.words[0].type.Longer +
                           " (which is a " + input.dependencies[1].depType.Longest +
                           ") and a " + input.words[1].type.Longer + ".\n")
            else:
                result += ("//NounPhrase out of a " + input.words[0].type.Longer +
                           "and a " + input.words[1].type.Longer +
                           " (which is a " + input.dependencies[1].depType.Longest + "). \n")
        else:
            if sameType != sameType:
                result += ("//NounPhrase out of a " + input.words[0].type.Longer + " and a" + input.words[
                    1].type.Longer + ".\n")
            else:
                result += ("//NounPhrase out of two " + input.words[0].type.Longer + "-s.\n")

        result += ("//NP2" + input.tree.tagTree[2:] + "\n")
        result += ("//" + input.tree.stanford + "\n")
        if len(input.dependencies) <= 1:
            result += ("NP -> undependent_" + input.words[1].type.Shortest.replace("basic", "") +
                   "_" + input.words[0].type.Shortest.replace("basic", "") +
                   "(" + input.words[1].type.Shortest +
                   "," + input.words[0].type.Shortest + ")\n")
        else:
            result += ("NP -> "+Digiter.toDigited(input.dependencies[1].depType.Shortest)+"_" + input.words[1].type.Shortest.replace("basic", "") +
                   "_" + input.words[0].type.Shortest.replace("basic", "") +
                   "(" + input.words[1].type.Shortest +
                   "," + input.words[0].type.Shortest + ")\n")


        result+="[string] *(?1,?2)\n"
        result += "[tree] NP2(?1,?2)\n"

        reverse = input.words[1].word == input.dependencies[0].endWord
        if connected:
            if not reverse:
                result += ("[ud] merge(f_dep(merge(\"(r<root> :" + input.dependencies[
                    1].depType.Shortest + " (d<dep>))\", r_dep(?2))),?1)\n")
            else:
                result += ("[ud] merge(f_dep(merge(\"(r<root> :" + input.dependencies[
                    1].depType.Shortest + " (d<dep>))\", r_dep(?1))),?2)\n")
        else:
            if not reverse:
                result += ("[ud] ?1\n")
            else:
                result += ("[ud] ?2\n")

        if connected:
            if input.dependencies[1].flangType == Fourlang._None:
                if not reverse:
                    result += ("[fourlang] ?2\n")
                else:
                    result += ("[fourlang] ?1\n")
            elif input.dependencies[1].flangType == Fourlang.OneBack_at_TwoTo:
                if not reverse:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/AT :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?1)))\n")
                else:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/AT :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?2)))\n")
            elif input.dependencies[1].flangType == Fourlang.OneBack_has_TwoTo:
                if not reverse:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/HAS :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?1)))\n")
                else:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/HAS :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?1))), r_dep1(?2)))\n")
            elif input.dependencies[1].flangType == Fourlang.OneBack__TwoTo:
                if not reverse:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root> :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?1)))\n")
                else:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root> :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?1))), r_dep1(?2)))\n")
            elif input.dependencies[1].flangType == Fourlang.OneTo_ZeroBack:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :1 (d<dep> :0 (r<root>)))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :1 (d<dep> :0 (r<root>)))\", r_dep(?1))),?2)\n")
            elif input.dependencies[1].flangType == Fourlang.Zero:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep> :0 (r<root>)))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep> :0 (r<root>)))\", r_dep(?1))),?2)\n")
            elif input.dependencies[1].flangType == Fourlang.ZeroFlat:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_flat (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_flat (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[1].flangType == Fourlang.ZeroCompound:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_compound (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_compound (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[1].flangType == Fourlang.ZeroTo:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[1].flangType == Fourlang.UnderTo:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :_ (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :_ (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[1].flangType == Fourlang.TwoTo:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :2 (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :2 (d<dep>))\", r_dep(?1))),?2)\n")
            else:
                if not reverse:
                    result += ("[fourlang] ?1\n")
                else:
                    result += ("[fourlang] ?2\n")
        else:
            if not reverse:
                result += ("[fourlang] ?1\n")
            else:
                result += ("[fourlang] ?2\n")
    return result


"""
1. Reading in the data
2. format the wordless trees
3. clean data from redundancy
4. sort the data into categories
5. generate the right text depending on the category
NP( VB( ), NN( ), NNS( ))
"""

#This is the function that generates 3 wide, 1 high NP-s.

def basicTernaryNPTail():
    reverse = False
    connected = False
    sameType = False

    result = ""
    datas = Data.fromFile("Data/Input/NP/np_1x3_trees", "Data/Input/NP/np_1x3_terms", "Data/Input/NP/np_1x3_deps", 2884)
    for input in datas:
        tmp=input.tree.wordLess.split(" ")
        input.tree.wordLess=tmp[0]+" ...( "+tmp[2]+" "+tmp[3]+" "+tmp[4]+" "+tmp[5]+" "+tmp[6]
    uniqData = {}
    for i in range(len(datas)-1,-1,-1):
        if not (uniqData.keys().__contains__(datas[i].tree.wordLess)):
            uniqData[datas[i].tree.wordLess] = datas[i]

    for input in uniqData.values():

        input.words.remove(input.words[2])

        place=-1
        for index in range(0,len(input.dependencies)):
            if ((input.dependencies[index].startWord == input.words[0].word and input.dependencies[index].endWord == input.words[1].word)
                    or (input.dependencies[index].startWord == input.words[1].word and input.dependencies[index].endWord == input.words[0].word)):
                place=index

        if place != -1:
            input.dependencies=[input.dependencies[place]]
        else:
            input.dependencies=[]

        result+="\n"
        connected = len(input.dependencies) ==1
        sameType = input.words[0].type.Shortest == input.words[1].type.Shortest
        if connected:
            reverse = input.words[1].word == input.dependencies[0].startWord

            if not reverse:
                result += ("//End of a NounPhrase out of a " + input.words[1].type.Longer +
                           " (which is a " + input.dependencies[0].depType.Longest +
                           ") and a " + input.words[0].type.Longer + ".\n")
            else:
                result += ("//End of a NounPhrase End out of a " + input.words[1].type.Longer +
                           "and a " + input.words[0].type.Longer +
                           " (which is a " + input.dependencies[0].depType.Longest + "). \n")
        else:
            if sameType != sameType:
                result += ("//End of a NounPhrase End out of a " + input.words[1].type.Longer +
                           " and a" + input.words[0].type.Longer + ".\n")
            else:
                result += ("//End of a NounPhrase End out of two " + input.words[0].type.Longer + "-s.\n")

        result += ("//NP3" + input.tree.tagTree[2:] + "\n")
        result += ("//" + input.tree.stanford + "\n")
        if len(input.dependencies)==1:
            result += ("NP_BAR -> "+Digiter.toDigited(input.dependencies[0].depType.Shortest)+"_" + input.words[1].type.Shortest.replace("basic", "") +
                   "_" + input.words[0].type.Shortest.replace("basic", "") +
                   "_Tail(" + input.words[1].type.Shortest +
                   "," + input.words[0].type.Shortest + ")\n")
        else:
            result += ("NP_BAR -> undependent_" + input.words[1].type.Shortest.replace("basic", "") +
                   "_" + input.words[0].type.Shortest.replace("basic", "") +
                   "_Tail(" + input.words[1].type.Shortest +
                   "," + input.words[0].type.Shortest + ")\n")

        result+="[string] *(?1,?2)\n"
        result += "[tree] NP3(*,?1,?2)\n"

        if connected:
            if not reverse:
                result += ("[ud] merge(f_dep(merge(\"(r<root> :" + input.dependencies[
                    0].depType.Shortest + " (d<dep>))\", r_dep(?2))),?1)\n")
            else:
                result += ("[ud] merge(f_dep(merge(\"(r<root> :" + input.dependencies[
                    0].depType.Shortest + " (d<dep>))\", r_dep(?1))),?2)\n")
        else:
            if not reverse:
                result += ("[ud] ?1\n")
            else:
                result += ("[ud] ?2\n")

        if connected:
            if input.dependencies[0].flangType == Fourlang._None:
                if not reverse:
                    result += ("[fourlang] ?2\n")
                else:
                    result += ("[fourlang] ?1\n")
            elif input.dependencies[0].flangType == Fourlang.OneBack_at_TwoTo:
                if not reverse:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/AT :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?1)))\n")
                else:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/AT :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?2)))\n")
            elif input.dependencies[0].flangType == Fourlang.OneBack_has_TwoTo:
                if not reverse:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/HAS :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?1)))\n")
                else:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/HAS :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?1))), r_dep1(?2)))\n")
            elif input.dependencies[0].flangType == Fourlang.OneBack__TwoTo:
                if not reverse:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root> :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?1)))\n")
                else:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root> :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?1))), r_dep1(?2)))\n")
            elif input.dependencies[0].flangType == Fourlang.OneTo_ZeroBack:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :1 (d<dep> :0 (r<root>)))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :1 (d<dep> :0 (r<root>)))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.Zero:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep> :0 (r<root>)))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep> :0 (r<root>)))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.ZeroFlat:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_flat (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_flat (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.ZeroCompound:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_compound (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_compound (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.ZeroTo:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.UnderTo:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :_ (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :_ (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.TwoTo:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :2 (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :2 (d<dep>))\", r_dep(?1))),?2)\n")
            else:
                if not reverse:
                    result += ("[fourlang] ?1\n")
                else:
                    result += ("[fourlang] ?2\n")
        else:
            if not reverse:
                result += ("[fourlang] ?1\n")
            else:
                result += ("[fourlang] ?2\n")
    return result
"""
NP( VB( ), NN( ), NNS( ))
"""
def basicTernaryNPComplete():
    reverse = False
    connected = False

    result = ""
    datas = Data.fromFile("Data/Input/NP/np_1x3_trees", "Data/Input/NP/np_1x3_terms", "Data/Input/NP/np_1x3_deps", 2884)
    for input in datas:
        tmp=input.tree.wordLess.split(" ")
        input.tree.wordLess=tmp[0]+" "+tmp[1]+" "+tmp[2]+" ...( "+tmp[4]+" ...( "+tmp[6]
    uniqData = {}
    for i in range(len(datas)-1,-1,-1):
        if not (uniqData.keys().__contains__(datas[i].tree.wordLess)):
            uniqData[datas[i].tree.wordLess] = datas[i]

    for input in uniqData.values():

        input.words.remove(input.words[1])
        input.words.remove(input.words[0])

        place=-1
        for index in range(0,len(input.dependencies)):
            if ((input.dependencies[index].startWord == input.words[0].word or input.dependencies[index].endWord == input.words[0].word)):
                place=index
                break

        if place != -1:
            input.dependencies=[input.dependencies[place]]
        else:
            input.dependencies=[]

        if(len(input.dependencies)==0 or input.dependencies[0].depType.Shortest=="root"):
            print("root")

        result+="\n"
        connected = len(input.dependencies) == 1
        if connected:
            reverse = input.words[0].word == input.dependencies[0].endWord

            if not reverse:
                result += ("//a long NounPhrase out of a " + input.words[0].type.Longer +
                           " (which is a " + input.dependencies[0].depType.Longest +
                           ") and a NounPhrase Bar.\n")
            else:
                result += ("//a long NounPhrase out of a  NounPhrase Bar and a " + input.words[0].type.Longer +
                           " (which is a " + input.dependencies[0].depType.Longest + "). \n")
        else:
            result += ("//a long NounPhrase out of a " + input.words[0].type.Longer +
                       " and a NounPhrase Bar.\n")

        result += ("//NP3" + input.tree.tagTree[2:] + "\n")
        result += ("//" + input.tree.stanford + "\n")
        if len(input.dependencies)==1:
            result += ("NP -> "+Digiter.toDigited(input.dependencies[0].depType.Shortest)+"_" + input.words[0].type.Shortest.replace("basic", "") +
                   "_NPBAR_Tail(" + input.words[0].type.Shortest +
                   ", NP_BAR)\n")
        else:
            result += ("NP -> unconnected_" + input.words[0].type.Shortest.replace("basic", "") +
                   "_NPBAR(" + input.words[0].type.Shortest +
                   ", NP_BAR)\n")

        result+="[string] *(?1,?2)\n"
        result += "[tree] @(?2,?1)\n"

        if connected:
            if not reverse:
                result += ("[ud] merge(f_dep(merge(\"(r<root> :" + input.dependencies[
                    0].depType.Shortest + " (d<dep>))\", r_dep(?2))),?1)\n")
            else:
                result += ("[ud] merge(f_dep(merge(\"(r<root> :" + input.dependencies[
                    0].depType.Shortest + " (d<dep>))\", r_dep(?1))),?2)\n")
        else:
            if not reverse:
                result += ("[ud] ?1\n")
            else:
                result += ("[ud] ?2\n")

        if connected:
            if input.dependencies[0].flangType == Fourlang._None:
                if not reverse:
                    result += ("[fourlang] ?2\n")
                else:
                    result += ("[fourlang] ?1\n")
            elif input.dependencies[0].flangType == Fourlang.OneBack_at_TwoTo:
                if not reverse:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/AT :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?1)))\n")
                else:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/AT :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?2)))\n")
            elif input.dependencies[0].flangType == Fourlang.OneBack_has_TwoTo:
                if not reverse:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/HAS :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?1)))\n")
                else:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root>/HAS :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?1))), r_dep1(?2)))\n")
            elif input.dependencies[0].flangType == Fourlang.OneBack__TwoTo:
                if not reverse:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root> :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?2))), r_dep1(?1)))\n")
                else:
                    result += (
                        "[fourlang] f_dep1(merge(f_dep2(merge(\"(r<root> :1 d1<dep1> :2 (d2<dep2>))\", r_dep2(?1))), r_dep1(?2)))\n")
            elif input.dependencies[0].flangType == Fourlang.OneTo_ZeroBack:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :1 (d<dep> :0 (r<root>)))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :1 (d<dep> :0 (r<root>)))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.Zero:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep> :0 (r<root>)))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep> :0 (r<root>)))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.ZeroFlat:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_flat (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_flat (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.ZeroCompound:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_compound (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0_compound (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.ZeroTo:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :0 (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.UnderTo:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :_ (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :_ (d<dep>))\", r_dep(?1))),?2)\n")
            elif input.dependencies[0].flangType == Fourlang.TwoTo:
                if not reverse:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :2 (d<dep>))\", r_dep(?2))),?1)\n")
                else:
                    result += ("[fourlang] merge(f_dep(merge(\"(r<root> :2 (d<dep>))\", r_dep(?1))),?2)\n")
            else:
                if not reverse:
                    result += ("[fourlang] ?1\n")
                else:
                    result += ("[fourlang] ?2\n")
        else:
            if not reverse:
                result += ("[fourlang] ?1\n")
            else:
                result += ("[fourlang] ?2\n")
    return result
