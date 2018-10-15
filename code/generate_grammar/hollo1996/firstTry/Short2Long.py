class Short2Long:
    sentencePart = {}
    dependency = {}

    def __init__(self, Shortest, Shorter, Longer, Longest):
        self.Shortest = Shortest;
        self.Shorter = Shorter;
        self.Longer = Longer;
        self.Longest = Longest;

    @classmethod
    def loadFromFile(cls, inputFileLocation, To):
        if To=="sentencePart":
            To=cls.sentencePart
        elif To=="dependency":
            To=cls.dependency

        with open(inputFileLocation, 'r') as file:
            lines = file.read().split('\n')
            key = ""

            for i in range(0,len(lines),5):
                keyLine=lines[i]
                if keyLine.endswith("basic"):
                    key = keyLine[0:len(keyLine) - 5]
                else:
                    key = keyLine
                To[key]=Short2Long(lines[i], lines[i+1],lines[i+2],lines[i+3])

    def str(self):
        return self.Shortest + "\n" + self.Shorter + "\n" + self.Longer + "\n" + self.Longest

    def getShortest(self):
        return self.Shortest
