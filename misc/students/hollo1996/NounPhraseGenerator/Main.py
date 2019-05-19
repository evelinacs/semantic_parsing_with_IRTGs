from tallNP import *

#This is my main file
#You can run this to watch how all NP-s are generated at the moment

Short2Long.loadFromFile("Data/Short2Long/sent_part_S2L", Short2Long.sentencePart)
Short2Long.loadFromFile("Data/Short2Long/dep_S2L", Short2Long.dependency)



with open("Data/Output/out_np_2x2_adjp.txt","w") as file:
    file.write(tallBinaryNPADJP())
with open("Data/Output/out_np_2x3_adjp_tail.txt","w") as file:
    file.write(tallTernaryNPADJPTail())
with open("Data/Output/out_np_2x3_adjp_comp.txt","w") as file:
    file.write(tallTernaryNPADJPComplete())
