#This is the class that replaces problematic characters

class Digiter:
    char2Name = {}

    @staticmethod
    def toDigited(withSymbols):
        if len(Digiter.char2Name) == 0:
            Digiter.char2Name[":"] = "_COLON_"
            Digiter.char2Name[","] = "_COMMA_"
            Digiter.char2Name["."] = "_PERIOD_"
            Digiter.char2Name[";"] = "_SEMICOLON_"
            Digiter.char2Name["-"] = "_HYPHEN_"
            Digiter.char2Name["["] = "_LSB_"
            Digiter.char2Name["]"] = "_RSB_"
            Digiter.char2Name["("] = "_LRB_"
            Digiter.char2Name[")"] = "_RRB_"
            Digiter.char2Name["{"] = "_LCB_"
            Digiter.char2Name["}"] = "_RCB_"
            Digiter.char2Name["!"] = "_EXC_"
            Digiter.char2Name["?"] = "_QUE_"
            Digiter.char2Name["'"] = "_SQ_"
            Digiter.char2Name["\\"] = "_BSL_"
            Digiter.char2Name["\""] = "_DQ_"
            Digiter.char2Name["/"] = "_PER_"
            Digiter.char2Name["#"] = "_HASHTAG_"
            Digiter.char2Name["%"] = "_PERCENT_"
            Digiter.char2Name["&"] = "_ET_"
            Digiter.char2Name["@"] = "_AT_"
            Digiter.char2Name["$"] = "_DOLLAR_"
            Digiter.char2Name["*"] = "_ASTERISK_"
            Digiter.char2Name["^"] = "_CAP_"
            Digiter.char2Name["`"] = "_IQ_"
            Digiter.char2Name["+"] = "_PLUS_"
            Digiter.char2Name["|"] = "_PIPE_"
            Digiter.char2Name["~"] = "_TILDE_"
            Digiter.char2Name["<"] = "_LESS_"
            Digiter.char2Name[">"] = "_MORE_"
            Digiter.char2Name["="] = "_EQ_"
            Digiter.char2Name["0"] = "_DIGIT_"
            Digiter.char2Name["1"] = "_DIGIT_"
            Digiter.char2Name["2"] = "_DIGIT_"
            Digiter.char2Name["3"] = "_DIGIT_"
            Digiter.char2Name["4"] = "_DIGIT_"
            Digiter.char2Name["5"] = "_DIGIT_"
            Digiter.char2Name["6"] = "_DIGIT_"
            Digiter.char2Name["7"] = "_DIGIT_"
            Digiter.char2Name["8"] = "_DIGIT_"
            Digiter.char2Name["9"] = "_DIGIT_"

        digited = "" + withSymbols
        for key in Digiter.char2Name:
            digited = digited.replace(key, Digiter.char2Name[key])
        while digited.__contains__("DIGIT__DIGIT"):
            digited=digited.replace("DIGIT__DIGIT", "DIGIT")
        digited = digited.replace("_DIGIT_", "_DIGITS_")
        digited = digited.replace("__", "_")
        return digited

    @staticmethod
    def toPuncted(textToPunct):
        textToPunct=textToPunct.replace("\n","")
        result = str(textToPunct)
        for value in Digiter.char2Name.values():
            if value != "_DIGIT_":
                while result.__contains__(value):
                    result = result.replace(value, "_PUNCT_")
        while result.__contains__("PUNCT_PUNCT"):
            result = result.replace("PUNCT_PUNCT", "PUNCT")
        if result == "_PUNCT_":
            result = "PUNCT"

        if result == "PUNCT":
            return "PUNCT"
        return textToPunct
