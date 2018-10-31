#!/bin/bash

#other="\(\S+ \S+\)"
other="\(\S+ [^\)]+\)"
adjp="\(ADJP( ${other})+\)"
adjp_or_other="(${adjp}|${other})"
subtrees="( ${adjp_or_other})+"
full_pattern="^\(NP${subtrees}\)$"

#echo "^\(NP( (\(ADJP( \(\S+ \S+\))+\)|\(\S+ \S+\)))+)$" # original pattern
#echo "${full_pattern}"

if [ "${2:-foo}" != "clean" ]; then
  grep -E "${full_pattern}" "${1}" | grep "ADJP"
else
  grep -E "${full_pattern}" "${1}" | grep "ADJP" | sed -E "s/${adjp}/(ADJP something)/"
fi

