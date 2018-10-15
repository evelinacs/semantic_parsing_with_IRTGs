from Short2Long import *
from Digiter import *


class Terminal:
    def __init__(self, type, word):
        self.type = type
        self.word = word

    # [('0.05', 'CD'), ('%', 'NN')]
    @staticmethod
    def fromString(terminal):
        terminal = str(terminal)

        terminal = terminal.replace("[('", "")
        terminal = terminal.replace("'), ('", "#")
        terminal = terminal.replace("\"), ('", "#")
        terminal = terminal.replace("'), (\"", "#")
        terminal = terminal.replace("\"), (\"", "#")
        terminal = terminal.replace("')]\n", "")
        terminal = terminal.replace("')]", "")
        dataParts = terminal.rsplit("#")

        result = []
        tmp = []

        for i in range(0, len(dataParts)):
            dataParts[i] = dataParts[i].replace("', '", "#")
            dataParts[i] = dataParts[i].replace("', \"", "#")
            dataParts[i] = dataParts[i].replace("\", '", "#")
            dataParts[i] = dataParts[i].replace("\", \"", "#")
            tmp = dataParts[i].split("#")

            tmp[1] = Digiter.toPuncted(Digiter.toDigited(tmp[1]))
            tmp[0] = Digiter.toDigited(tmp[0])

            result.insert(0,Terminal(Short2Long.sentencePart[tmp[1]], tmp[0]))

        return result


