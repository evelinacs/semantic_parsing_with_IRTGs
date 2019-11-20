# semantic_parsing_with_IRTGs

This repository contains our experiments of developing an IRTG ([Interpreted Regular Tree Grammar](http://delivery.acm.org/10.1145/2210000/2206331/p2-koller.pdf?ip=152.66.170.27&id=2206331&acc=OPEN&key=C8586E1EAA35B39B%2ECEAA96605014474A%2E4D4702B0C3E38B35%2E6D218144511F3437&__acm__=1537872342_0c80d269c92c583e0edf1017078efeae)) which implements a mapping between the output of the [Stanford Parser](https://nlp.stanford.edu/software/lex-parser.shtml), [Universal Dependencies](http://universaldependencies.org/) v2.1 and [4lang](https://github.com/kornai/4lang).

Our system for [Surface Realization Shared Task 2019](https://taln.upf.edu/pages/msr2019-ws/SRST.html) can be found [here](https://github.com/adaamko/surface_realization).

# Python virtual environment

Whenever possible, all code should be written in Python3 and use the repository's virtual environment.

## Creating the virtual environment

### With virtualenvwrapper

```shell
mkvirtualenv -p python3 irtg
```

### Without virtualenvwrapper

```shell
python3 -m venv .venv
```

If the default python executable is Python3 (e.g. on Windows):

```shell
python -m venv .venv
```

## Activating the virtual environment

### With virtualenvwrapper

```shell
workon irtg
```

### Without virtualenvwrapper

#### Linux

```shell
. .venv/bin/activate
```

#### Windows

Using `CMD.exe`:

```cmd
.venv\Scripts\activate.bat
```

Using `powershell`:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Installing the required modules

After activating the virtual environment:

```shell
pip install -r requirements.txt
```

## Deactivating the virtual environment

```shell
deactivate
```

# [Alto](https://github.com/coli-saar/alto) console usage

``` shell 
java -cp "<path to ALTO's jar>" de.up.ling.irtg.script.ParsingEvaluator "<path to input file>" -g "<path to the grammar file>" -I "<input format>" -O "<output format>" -o "<output file>"
```
