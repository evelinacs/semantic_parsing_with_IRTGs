from Data import *
"""
        //VerbPhrase out of one Word
        //VP(WD(stuff))
        VP -> one_WD(WD)
        [tree] VP(?1)
        [ud] ?1
        [fourlang] ?1
"""

# unary VPs

def basicUnaryVP():
    result=""

    datas=Data.fromFile("data/Input/Unary/unary_vp_trees", "data/Input/Unary/unary_vp_terms", "data/Input/Unary/unary_vp_deps", 26)
    uniqData={}
    for i in range(len(datas)-1,-1,-1):
        if not (uniqData.keys().__contains__(datas[i].tree.wordLess)):
            uniqData[datas[i].tree.wordLess]=datas[i]

    for input in uniqData.values():
        result+="\n"
        result+="//VerbPhrase out of one " + input.words[0].type.Longer + ".\n"
        result+="//" + input.tree.stanford+"\n"
        result+="//" + input.tree.tagTree+"\n"
        result+="VP -> one_" + input.words[0].type.Shortest.replace("basic", "") + "(" + input.words[0].type.Shortest + ")\n"
        result+="[string] ?1\n"
        result+="[tree] VP(?1)\n"
        result+="[ud] ?1\n"
        result+="[fourlang] ?1\n"
    return result
