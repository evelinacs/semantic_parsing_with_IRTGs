#!/usr/bin/env python
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader import *
#import json

orig_pattern = r'(wsj/\d\d/wsj_\d\d|brown/c[a-z]/c[a-z])\d\d.mrg'
#mrg_pattern = r'(atis|brown|swbd|wsj)/([^/]+/)*[^.]+\.mrg'
mrg_pattern = r'(wsj)/([^/]+/)*[^.]+\.mrg'
ptb = LazyCorpusLoader(
    'ptb',
    CategorizedBracketParseCorpusReader,
    mrg_pattern,
    cat_file='allcats.txt',
    tagset='wsj',
)
#print(json.dumps(ptb.fileids(), indent=2))

