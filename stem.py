#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from util import getfnames,punc
import codecs,os.path,os
from collections import defaultdict

def stem(fof, endingsfname, outfof="", col=5):
    fnames = getfnames(fof)

    with codecs.open(endingsfname, "r", "utf8") as f:
        line = f.read()
        endings = line.split()

    removals = defaultdict(int)
        
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
                stillgoing = True
                while stillgoing:
                    stillgoing = False
                    for ending in endings:
                        if w.endswith(ending):
                            w = w[:-len(ending)]
                            stillgoing = True
                            removals[ending] += 1
                if len(w.strip()) > 0:
                    sline[col] = w.strip()

            out.write("\t".join(sline))
            
        out.close()
        print("Wrote to: ", outname)
        
    print("Histogram of removals: ")
    out2 = codecs.open("tmp", "w", "utf8")
    for ending in removals:
        print(ending + ": " + str(removals[ending]))
        out2.write(ending + "\t" + str(removals[ending]) + "\n")
    out.close()
    
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("fof",help="folder to stem")
    parser.add_argument("outfof",help="empty folder to write to (typically call this ???-stem)")
    parser.add_argument("endings",help="filename of endings, separated by space.")
    parser.add_argument("--col",help="which column to change.", type=int, default=5)
    
    args = parser.parse_args()
    
    stem(args.fof, args.endings, args.outfof, args.col)
