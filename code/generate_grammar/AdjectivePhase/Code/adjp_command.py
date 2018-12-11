#from unidecode import unidecode
#-*- coding: utf-8 -*-
import sys
import re
import re
from nltk.corpus import treebank

dep=[]
dep_help=[]


#A leparszolt dependencia blokkok beolvasasa (D:/Onlab/ADJP_generalas/Input/adjp_output_deps.txt)
with open(sys.argv[1]) as f:
    line=f.readlines()

for i in line:
    if i!="----------\n":
        dep_help.append(i)
    else:
        dep.append(dep_help)
        dep_help=[]
        
#a dependenciablokkbol kiolvasva a szukseges neveket
dependencies=[]
for i in range (0, len(dep)):
    dependencies.append(re.findall(r"[a-zA-Z]+\(", str(dep[i][0])))
for j in range (0, len(dependencies)):
        for k in range (0, len(dependencies[j])):
            dependencies[j][k]=dependencies[j][k].replace('(','')

for j in range (0, len(dependencies)):
    for k in range (0, len(dependencies[j])):
        if (dependencies[j][k]=='but' or dependencies[j][k]=='and' or dependencies[j][k]=='or' or dependencies[j][k]=='by' or dependencies[j][k]=='on'):
            dependencies[j][k]=dependencies[j][k].replace(dependencies[j][k],'conj')
        


#extract_subtrees.py futtatasa utan kapott eredmeny
#ket sor torlesre kerult (233, 278), mert a dependencianal nem sikerul
#ezeket leparszolni
#D:/Onlab/ADJP_generalas/Input/adjp_output.txt

with open(sys.argv[2]) as l:
    adjplist=l.readlines()

#ADJP members letrehozasa: ADJP, NP, CP, NNS, JJ
adjpmembers=[]  
for i in range (0, len(adjplist)):
    adjpmembers.append(re.findall(r"\([a-zA-Z]+", str(adjplist[i])))
for j in range (0, len(adjpmembers)):
        for k in range (0, len(adjpmembers[j])):
            adjpmembers[j][k]=adjpmembers[j][k].replace('(','')


adjp=[]
for i in range (0, len(adjpmembers)):
	adjp.append(adjpmembers[i])
	for j in range(0, len(dependencies[i])):
		adjp[i].append(dependencies[i][j])

#adjp unary, binary, ternary kulon kigyujtese a konnyebb kezelhetes erdekeben
adjp_unary=[]
adjp_binary=[]
adjp_ternary=[]

for i in range (0, len(adjp)):
    length = len(adjp[i])
    if (length==3):
         adjp_unary.append(adjp[i])
    if (length==5):
        adjp_binary.append(adjp[i])
    if (length==7):
        adjp_ternary.append(adjp[i])
    
# duplikaltsagok megszuntetese
adjp_unary = list(set(map(tuple, adjp_unary)))
adjp_binary = list(set(map(tuple, adjp_binary)))
adjp_ternary = list(set(map(tuple, adjp_ternary)))

# 
def bi_dependencies(adjp_item, number):
    if adjp_item[number][3]=='root':
        return adjp_item[number][4]
    else:
        return adjp_item[number][3]

def tri_dependencies(adjp_item, number):
    if adjp_item[number][4]=='root':
        return [adjp_item[number][5], adjp_item[number][6]]
    if adjp_item[number][5]=='root':
        return [adjp_item[number][4], adjp_item[number][6]]
    else:
        return [adjp_item[number][4], adjp_item[number][5]]

def gen_unary(adjp_sentence, number):
    result = str(adjp_sentence[number][0]) + ' -> dep_'+str(adjp_sentence[number][1])+'(' + str(adjp_sentence[number][1]) + ')\n'
    result+= '[tree] ?1 \n'
    result+= '[ud] ?1 \n'
    result+= '[fourlang] ?1 \n\n'
    return result 
                
                
def gen_binary(adjp_sentence, number):
    result = str(adjp_sentence[number][0]) + ' -> dep_' +str(adjp_sentence[number][1])+'_'+ str(adjp_sentence[number][2])+'('+ str(adjp_sentence[number][1]) + ', ' + str(adjp_sentence[number][2]) + ')\n'
    result+= '[tree] ' + adjp_sentence[number][0] + '2' + '(?2, ?1) \n' 
    result+= '[ud] f_dep(merge_root_dep(merge("(r<root> :' + bi_dependencies(adjp_sentence, number) +'(d<dep>))", ?1), ?2))\n'
    result+= '[fourlang] f_dep(merge_root_dep(merge("(r<root> :0 (d<dep>))", ?1), ?2)) \n\n'
    return result

def gen_ternary(adjp_sentence, number):
    a=tri_dependencies(adjp_sentence, number)
    result = str(adjp_sentence[number][0]) + ' -> dep_'+ str(adjp_sentence[number][1]) + '_' + str(adjp_sentence[number][2]) +  '_' + str(adjp_sentence[number][3])+'(' + str(adjp_sentence[number][1]) + ', ' + str(adjp_sentence[number][2]) +  ', ' + str(adjp_sentence[number][3]) +')\n'
    result+= '[tree] ' + adjp_sentence[number][0] + '3' + '(?3, ?2, ?1) \n' 
    result+= '[ud] f_dep2(f_dep1(merge(merge(merge(?1,"(r<root> : ' + a[0] + '(d1<dep1>) :' + a[1] +'(d2<dep2>)))"), r_dep1(?2)), r_dep2(?3))))\n'
    result+= '[fourlang] f_dep2(f_dep1(merge(merge(merge(?1,"(d2<dep2> :0 (r<root>) :0 (d1<dep1>))"), r_dep1(?2)), r_dep2(?3)))) \n\n'
    return result

def write_file(output):
    with open(sys.argv[3], 'a') as of:
        of.write(output)

def main():
    with open(sys.argv[3], 'w') as outputfile:
        write_file('interpretation tree: de.up.ling.irtg.algebra.TagTreeAlgebra \n'+
               'interpretation ud: de.up.ling.irtg.algebra.graph.GraphAlgebra \n'+
               'interpretation fourlang: de.up.ling.irtg.algebra.graph.GraphAlgebra \n\n'+
               '//rules \n'+
               '//Unary \n'+
               '//Start sentence \n\n'+
               'S! -> _adjmod(ADJP) \n'+
               '[tree] ADJP(?1) \n'+
               '[ud] ?1 \n'+
               '[fourlang] ?1 \n\n')

    for i in range (0, len(adjp_unary)):
        write_file(gen_unary(adjp_unary, i))

    for j in range (0, len(adjp_binary)):
        write_file(gen_binary(adjp_binary, j))

    for k in range (0, len(adjp_ternary)):
        write_file(gen_ternary(adjp_ternary, k))

if __name__=="__main__":
    main()


