[string] *(?1,?2)
[tree] {treenode}(*,?1,?2)
[ud] merge(f_dep(merge("(r<root> :{ud_edge} (d<dep>))", r_dep({ud_dep}))),{ud_root})
[fourlang] f_dep1(merge(f_dep2(merge("(r<root> :{4lang_edge} d1<dep1> :{4lang_edge2} (d2<dep2>))", r_dep2({4lang_dep2}))), r_dep1({4lang_dep1})))
