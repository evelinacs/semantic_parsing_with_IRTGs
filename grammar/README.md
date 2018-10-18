##ALTO console usage
description: ALTO is tricky to use, but we figured out, so here you are. We give an example for imput file too.

Use this command:java -cp <path to ALTO's jar> de.up.ling.irtg.script.ParsingEvaluator <path to inputfile> -g <path to one of the irtg's> -I tree

forExample:java -cp "alto-2.2-SNAPSHOT-jar-with-dependencies.jar" de.up.ling.irtg.script.ParsingEvaluator input_example_1 -g "NewSolution_(stable).irtg" -I tree

#grammar
description: This folder contains the **IRTG grammars**

includes:
## hollo1996
description: This is the folder for Holló-Szabó Ákos's irtgs made for NP-s. They include templates, grammers with four algebra, and examples for semantic and syntactic prevarications.

includes:
###complete
description:This folder contains the **demo ready IRTG grammars**

###under_test
description:This folder contains the **IRTG grammars under test**
includes:
####NP_1x1_test.irtg
created:2018.10.17
description:This is the grammer for the most simple Noun Phrases.
usage:use for example NP(NN(cat)) as an input
####NP_1x2_test.irtg
created:2018.10.17
description:This is the grammer for the most simple Noun Phrases.
usage:use for example NP(JJ(big)NN(cat)) as an input
####NP_1x3_test.irtg
created:2018.10.17
description:This is the grammer for the most simple Noun Phrases.
usage:use for example NP(CD(nine)JJ(big)NN(cat)) as an input
####TFB_Cleric_Test.irtg
created:2018 summer
description:This is the grammer for our first example for syntactic ambiguaty.
usage:not functioning yet

###templates
description:This folder contains the **IRTG grammars templates**. They are needed to achive nicely formated uniform grammers, whitch we can merge any time easily.
includes
####main_Template.irtg
created:2018 summer
description:This is the file we can use to build a usual nicely functioning and looking grammer for whole sentences. 
####NP_Template.irtg
created:2018 summer
description:This is the file we can use to build a nicely functioning and looking grammer for noun phrases.
 




