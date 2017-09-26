#!/usr/bin/python
# -*- coding: utf-8 -*-
from util import getfnames,punc
import codecs,os.path,os
from collections import defaultdict

###
# This operates similar to stem.py except that the input is a file (probably from Upenn, Hongzhi Xu)
# that maps words to their stemmed versions (as opposed to a freeform list of stems).

def stem(fof, endingsfname, outfof="", col=5):
    fnames = getfnames(fof)

    replace = {}
    with codecs.open(endingsfname, "r", "utf8") as f:
        for line in f:
            sline = line.split("\t")
            if len(sline) != 3:
                continue
            word, seg, comps = sline
            #print(word, seg, comps)
            if len(comps.split()) > 0:
                stem = comps.split()[0]
                replace[word] = stem

    numreplaced = 0
    
    for fname in fnames:
        with codecs.open(fname, "r", "utf8") as f:
            lines = f.readlines()
            
        fnonly = os.path.basename(fname)
            
        outname = os.path.join(outfof, fnonly)        
        out = codecs.open(outname, "w", "utf8")
        
        i = 1
        for line in lines:
            if line[0] == "#":
                out.write(line)
                continue

            sline = line.split("\t")
            if len(sline) > col:            
                w = sline[col]
                if w in replace and replace[w] is not w:
                    numreplaced += 1
                    sline[col] = replace[w]
        
            out.write("\t".join(sline))
            
        out.close()
        print("Wrote to: ", outname)

    print("numreplaced: ", numreplaced)
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("fof",help="folder to stem")
    parser.add_argument("outfof",help="empty folder to write to (typically call this ???-stem)")
    parser.add_argument("endings",help="file mapping (probably from UPenn, Hongzhi Xu)")
    parser.add_argument("--col",help="which column to change.", type=int, default=5)
    
    args = parser.parse_args()
    
    stem(args.fof, args.endings, args.outfof, args.col)
