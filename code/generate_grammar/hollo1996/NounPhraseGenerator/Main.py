from basicNP import *

#This is my main file
#You can run this to watch how all NP-s are generated at the moment

Short2Long.loadFromFile("Data/Short2Long/sent_part_S2L", Short2Long.sentencePart)
Short2Long.loadFromFile("Data/Short2Long/dep_S2L", Short2Long.dependency)


with open("Data/Output/out_np_1x1.txt","w") as file:
    file.write(basicUnariNP())
with open("Data/Output/out_np_1x2.txt","w") as file:
    file.write(basicBinaryNP())
with open("Data/Output/out_np_1x3_tail.txt","w") as file:
    file.write(basicTernaryNPTail())
with open("Data/Output/out_np_1x3_comp.txt","w") as file:
    file.write(basicTernaryNPComplete())
