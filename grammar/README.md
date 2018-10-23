# ALTO console usage

Use this command:

``` shell 
java -cp "<path to ALTO's jar>" de.up.ling.irtg.script.ParsingEvaluator "<path to input file>" -g "<path to the grammar file>" -I "<input format>" -O "<output format>" -o "<output file>"
```

for example:

```shell
 java -Xmx16G -cp alto-2.1.jar de.up.ling.irtg.script.ParsingEvaluator "unary_nps_input_trees" -g "NP_1x1_test.irtg" -I tree -O ud=amr-sgraph -O fourlang=amr-sgraph -O string=toString -o "np_parse"
```

# grammar

This folder contains the **IRTG grammars**

## hollo1996

This is the folder for Holló-Szabó Ákos's irtgs made for NP-s, templates and grammars with four algebras.

### complete

This folder contains the **demo ready IRTG grammars**

### under_test

This folder contains the **IRTG grammars under test**

#### NP_1x1_test.irtg

- created: 2018-10-17
- description: This is the grammar for the simplest (e.g. consisting of only one word) NPs.
- usage: use for example `NP(NN(cat))` as an input

#### NP_1x2_test.irtg

- created: 2018-10-17
- description: Grammar for 2-wide NPs.
- usage: use for example `NP(JJ(big)NN(cat))` as an input

#### NP_1x3_test.irtg

- created: 2018-10-17
- description: Grammar for 3-wide NPs.
- usage: use for example `NP(CD(nine)JJ(big)NN(cat))` as an input

#### TFB_Cleric_Test.irtg

- created: summer of 2018
- description: Example grammar for syntactic ambiguity.
- usage: not functioning yet

### templates

This folder contains the **IRTG grammar templates** for generating uniform grammars.

#### main_Template.irtg

- created: summer of 2018
- description: template for full sentences

#### NP_Template.irtg

- created: summer of 2018
- description: template for NPs
