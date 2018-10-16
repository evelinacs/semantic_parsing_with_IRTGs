from Short2Long import *
from basicUnaryNP import *
from basicBinaryNP import *
from basicTernaryNP import *

#This is my main file
#You can run this to watch how all NP-s are generated at the moment

Short2Long.loadFromFile("data/Short2Long/sentencePartS2L", Short2Long.sentencePart)
Short2Long.loadFromFile("data/Short2Long/dependencyS2L", Short2Long.dependency)


with open("data/Output/OutUnary.txt","w") as file:
    file.write(basicUnariNP())
with open("data/Output/OutBinary.txt","w") as file:
    file.write(basicBinaryNP())
with open("data/Output/OutTernary_Tail.txt","w") as file:
    file.write(basicTernaryNPTail())
with open("data/Output/OutTernary_Complete.txt","w") as file:
    file.write(basicTernaryNPComplete())
