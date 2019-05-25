import sys
from collections import defaultdict

def check_name(gold_words, parse_words, pos_lemma_sets):
    if len(gold_words) != len(parse_words):
        return False
    
    for word in parse_words:
        if not (word in pos_lemma_sets["NNP"] or word in pos_lemma_sets["NNPS"]):
            return False
    return True

def check_jj(gold_words, parse_words, pos_lemma_sets):
    if len(gold_words) != 2 or len(parse_words) != 2:
        return False
    
    jj_set = pos_lemma_sets["JJ"]
    nn_set = pos_lemma_sets["NN"]
    nns_set = pos_lemma_sets["NNS"]

    if gold_words[0] in jj_set and (gold_words[1] in nn_set or gold_words[1] in nns_set):
        if parse_words[1] in jj_set and (parse_words[0] in nn_set or parse_words[0] in nns_set):
            return True
    elif gold_words[1] in jj_set and (gold_words[0] in nn_set or gold_words[0] in nns_set):
        if parse_words[0] in jj_set and (parse_words[1] in nn_set or parse_words[1] in nns_set):
            return True
    
    return False

def check_dt(gold_words, parse_words, pos_lemma_sets):
    gold_no_dt = [x for x in gold_words if x not in pos_lemma_sets['DT']]
    parse_no_dt = [x for x in parse_words if x not in pos_lemma_sets['DT']]
    
    return tuple(gold_no_dt) == tuple(parse_no_dt)

def check_jj_jj(gold_words, parse_words, pos_lemma_sets):
    gold_jj = []
    for x in gold_words:
        if x in pos_lemma_sets['JJ']:
            gold_jj.append('JJ')
        elif x in pos_lemma_sets['NN'] or x in pos_lemma_sets['NNS']:
            gold_jj.append('NN')
        else:
            gold_jj.append(x)
    
    parse_jj = []
    for x in parse_words:
        if x in pos_lemma_sets['JJ']:
            parse_jj.append('JJ')
        elif x in pos_lemma_sets['NN'] or x in pos_lemma_sets['NNS']:
            parse_jj.append('NN')
        else:
            parse_jj.append(x)
    
    gold_jj = " ".join(gold_jj)
    parse_jj = " ".join(parse_jj)
    if gold_jj == parse_jj:
        if -1 < gold_jj.find('JJ JJ NN'):
            return True
    
    return False


def compare(fn1, fn2, fn3):
    with open(fn1) as gold_file, open(fn2) as parse_file, open(fn3) as conll_file:
        pos_lemma_sets = defaultdict(set)
        for line in conll_file:
            if line.startswith("#") or line == "\n":
                continue
            fields = line.split("\t")
            lemma = fields[2]
            pos = fields[4]
            pos_lemma_sets[pos].add(lemma)

        
        output = []
        ok_count = 0
        null_count = 0
        bad_count = 0
        name_count = 0
        jj_count = 0
        dt_count = 0
        jj_jj_count = 0
        for i, gold_line in enumerate(gold_file):
            parse_line = parse_file.readline()

            if gold_line.lower() == parse_line.lower():
                ok_count += 1
            elif parse_line == "<null>\n":
                null_count += 1
            else:
                bad_count += 1
                gold_words = gold_line.strip().split(" ")
                parse_words = parse_line.strip().split(" ")
                
                tags = ["# Tags:"]
                if check_name(gold_words, parse_words, pos_lemma_sets):
                    name_count += 1
                    tags.append("#name")
                if check_jj(gold_words, parse_words, pos_lemma_sets):
                    jj_count += 1
                    tags.append("#JJ_NN")
                if check_dt(gold_words, parse_words, pos_lemma_sets):
                    dt_count += 1
                    tags.append("#DT")
                if check_jj_jj(gold_words, parse_words, pos_lemma_sets):
                    jj_jj_count += 1
                    tags.append("#JJ_JJ")

                output.append("# ID: {}\n".format(i + 1))
                output.append("{}\n".format(" ".join(tags)))
                output.append(gold_line)
                output.append(parse_line)
                output.append("\n")
        
        print("# ALL: {}; OK: {}; BAD: {}; NULL: {}".format(i + 1, ok_count, bad_count, null_count))
        print("# Names in wrong order: {}".format(name_count))
        print("# JJ in wrong order: {}".format(jj_count))
        print("# JJ JJ in wrong order: {}".format(jj_jj_count))
        print("# DT in wrong place: {}".format(dt_count))
        print()
        print("".join(output))

compare(sys.argv[1], sys.argv[2], sys.argv[3])