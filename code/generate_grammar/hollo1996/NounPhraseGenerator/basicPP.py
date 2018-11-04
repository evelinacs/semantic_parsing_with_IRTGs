from Data import *
"""
        //PrepositionalPhrase out of one Word
        //PP(WD(stuff))
        PP -> one_WD(WD)
        [tree] VP(?1)
        [ud] ?1
        [fourlang] ?1
"""

# unary PPs

def basicUnaryPP():
    result=""

    datas=Data.fromFile("Data/Input/PP/np_1x1_trees", "Data/Input/PP/np_1x1_terms", "Data/Input/PP/np_1x1_deps", 3)
    uniqData={}
    for i in range(len(datas)-1,-1,-1):
        if not (uniqData.keys().__contains__(datas[i].tree.wordLess)):
            uniqData[datas[i].tree.wordLess]=datas[i]

    for input in uniqData.values():
        result+="\n"
        result+="//PrepositionalPhrase out of one " + input.words[0].type.Longer + ".\n"
        result+="//" + input.tree.stanford+"\n"
        result+="//" + input.tree.tagTree+"\n"
        result+="PP -> one_" + input.words[0].type.Shortest.replace("basic", "") + "(" + input.words[0].type.Shortest + ")\n"
        result+="[string] ?1\n"
        result+="[tree] PP(?1)\n"
        result+="[ud] ?1\n"
        result+="[fourlang] ?1\n"
    return result
