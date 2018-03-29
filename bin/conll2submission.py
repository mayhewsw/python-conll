#!/home/mayhew2/miniconda3/bin/python
import os,codecs
from collections import defaultdict
from conll.readconll import *



def outline(menid, mention,docid,start,end,label):
    return "\t".join(["UPENN",menid,mention,docid+":"+str(start)+"-"+str(end),"NULL", label, "NAM", "1.0"])
    

def func(folder, outfile):
    fnames = os.listdir(folder)
    nowbreak = False
    menid = 0
    i = 0
    outlines = []
    for fname in fnames:
        #print(fname)
        if i%100 == 0:
            print("on {} out of {}".format(i, len(fnames)))
        cdoc = readconll(folder + "/" + fname)

        i += 1
        for c in cdoc.getconstituents():
            #print(span, label)
            span = c.span
            label = c.label
            mention = cdoc.getString(span)
            nowbreak=True
            start,end = cdoc.getCharSpan(span)
            docid = fname.split(".")[0]

            ol = outline("mention" + str(menid),mention,docid,start,end,label)
            outlines.append(ol)
            menid += 1
            
    with open(outfile, "w") as out:
        for line in outlines:
            out.write(line + "\n");

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("folder",help="")
    parser.add_argument("outfile",help="")

    args = parser.parse_args()
    
    func(args.folder, args.outfile)
