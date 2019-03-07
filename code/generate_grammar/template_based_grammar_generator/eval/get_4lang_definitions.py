import sys
import json

"""
Should be used on longman_firsts.json
"""

def get_4lang_definitions(fn):
    with open(fn) as def_json:
        data = json.load(def_json)
        for word, entry in data.items():
            for sense in entry["senses"]:
                if sense["definition"] is not None:
                    print(sense["definition"]["sen"] + ".")

get_4lang_definitions(sys.argv[1])

