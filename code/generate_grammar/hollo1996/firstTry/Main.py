from Short2Long import *
from basicUnaryNP import *
from basicBinaryNP import *
from basicTernaryNP import *

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

"""
			Console.WriteLine("Add meg a fát");
			string input = Console.ReadLine();
			Tree output = Tree.fromString(input);

			Console.WriteLine(output.stanford);
			Console.WriteLine(output.wordLess);
			Console.WriteLine(output.tagTree);
            for (int i = 0; i < output.words.Length; i++)
			{
				Console.WriteLine(output.words[i]);            
			}
"""

"""     

        /*


        /*
        //complete
        //

        //NounPhrase starting with a Word (whitch is a Modifier).
        //NP (WD(stuff), WD1(stuff), WD2(stuff))
        NP -> mod_WD_NBAR(WD, N_BAR)
        [tree] @(?2,?1)
        [ud] merge(f_dep(merge("(r<root> :mod (d<dep>))", r_dep(?1))),?2)
        [fourlang] merge(f_dep(merge("(r<root> :_ (d<dep>))", r_dep(?1))),?2)

        //tail
        //

        //NounBar Out of a Word1 (whitch is a Modifier1) and a Word2.
        //(NP (WD1 stuff) (WD2 stuff))
        N_BAR -> mod1_WD1_WD2_Part(WD1, WD2)
        [tree] NP3(*,?1,?2)
        [ud] merge(f_dep(merge("(r<root> :mod1 (d<dep>))", r_dep(?1))),?2)
        [fourlang] merge(f_dep(merge("(r<root> :_ (d<dep>))", r_dep(?1))),?2)
        */
        private static List<string> basicTernaryNPtail(string from, string to)
        {
            List<string> result = new List<string>();
            //TODO
            return result;
        }
        private static List<string> basicTernaryNPcomplete(string from, string to)
        {
            List<string> result = new List<string>();
            //TODO
            return result;
        }
    }
}

"""
