#!/bin/bash

# script for making input out of phrase structure trees
# max 3 width
# usage: bash make_alto_input.sh phrase_level > output
# phrase_level: the name of the phrase level to extract, e.g. NP, ADJP

TMP_STEP1_SUBTREE="/tmp/tmp_step1_subtree"
TMP_STEP2_FILTERED="/tmp/tmp_step2_filtered"
TMP_STEP3_SORTED="/tmp/tmp_step3_sorted"
TMP_STEP4_FORMATTED="/tmp/tmp_step4_formatted"

phrase_level="${1}"
phrase_level_list="ADJP|ADVP|CONJP|FRAG|INTJ|LST|NAC|NP|NX|PP|PRN|PRT|QP|RRC|UCP|VP|WHADJP|WHAVP|WHNP|WHPP|X"

python extract_subtrees.py -s "${phrase_level}" > "${TMP_STEP1_SUBTREE}"
python filter_tree.py "${TMP_STEP1_SUBTREE}" > "${TMP_STEP2_FILTERED}"
bash sort.sh "${TMP_STEP2_FILTERED}" > "${TMP_STEP3_SORTED}"
python format_tree.py "${TMP_STEP3_SORTED}" > "${TMP_STEP4_FORMATTED}"
cat "${TMP_STEP4_FORMATTED}" | grep -v -E "((${phrase_level_list})[4-9]\()"

rm "${TMP_STEP1_SUBTREE}"
rm "${TMP_STEP2_FILTERED}"
rm "${TMP_STEP3_SORTED}"
rm "${TMP_STEP4_FORMATTED}"
