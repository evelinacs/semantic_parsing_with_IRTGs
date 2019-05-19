[string] *(?1,?2)
[tree] {treenode}({treechildren})
[ud] merge(f_dep(merge("(r<root> :{ud_edge} (d<dep>))", r_dep({ud_dep}))),{ud_root})
[fourlang] f_dep(merge(merge({4lang_root}, "({4langnode} :1 (d<dep>) :2 (r<root>))"), r_dep({4lang_dep})))
