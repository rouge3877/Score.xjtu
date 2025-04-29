from jwapp import *

s=Student(2204112913)
a=Address(s)
cclass="操作系统"
l=a.reset().goto("教学班",cclass).list_id()

sl=StudentList(l)

t=sl.scores_detail(cclass)

t=t.sort_values("score",ascending=False)

t.to_csv("score.csv")
