# Convert conllu file to isi file
python conllu_to_isi.py NPS.conllu > NPS.conllu.isi
# Mark trees that were not parsed by v2 in the .isi file with a <none> line
python align_data.py 3np_large_filtered NPS.conllu.isi > NPS.conllu.isi.aligned
# Filter <none> lines from both tree and isi files
python filter_none.py 3np_large_filtered 3np_large_aligned NPS.conllu.isi.aligned 3np_large_aligned_dep