from Data import *
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

    datas=Data.fromFile("data/Input/Unary/basicUnary_Trees", "data/Input/Unary/basicUnary_Terminals", "data/Input/Unary/basicUnary_Dependencies", 1642)
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
