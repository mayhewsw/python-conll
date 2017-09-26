#!/home/mayhew2/miniconda3/bin/python
import sys
import os,codecs
from collections import defaultdict
from conll.readconll import *

files = os.listdir(sys.argv[1])

myset = defaultdict(int)

for f in files:
    cdoc = readconll(sys.argv[1] + "/" + f)
    t = cdoc.tokens

    for c in cdoc.getconstituents():
        myset[c.label + "\t" + c.surf()] += 1


sss = sorted(myset.items(), key=lambda p: p[1], reverse=True)

sm = 0
for s in sss:
    num = s[1]
    #print(s[0] + num)
    sm += num

print("Num unique names:", len(sss))
print("Avg num repetitions", sm / float(len(sss)))
print("Unique / Total", len(sss)/ float(sm))

with open("names.txt", "w") as out:
    for n in sss:
        out.write("\t".join(map(str, n)) + "\n")
