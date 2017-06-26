#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from util import getfnames,punc
import codecs,os.path,os
from collections import defaultdict

def stem(fof, prefixfname, suffixfname, outfof="", col=5):
    fnames = getfnames(fof)

    prefixes = []
    if prefixfname:
        with codecs.open(prefixfname, "r", "utf8") as f:
            for line in f:
                prefixes.append(line.split()[0])

    suffixes = []
    if suffixfname:
        with codecs.open(suffixfname, "r", "utf8") as f:
            for line in f:
                suffixes.append(line.split()[0])

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

                # first do prefixes
                stillgoing = True
                while stillgoing:
                    stillgoing = False
                    for pref in prefixes:
                        if w.startswith(pref):
                            w = w[len(pref):]
                            stillgoing = True
                            removals[pref + "-"] += 1

                # then do suffixes
                stillgoing = True                
                while stillgoing:
                    stillgoing = False
                    for ending in suffixes:
                        if w.endswith(ending):
                            w = w[:-len(ending)]
                            stillgoing = True
                            removals["-" + ending] += 1
                
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

    parser.add_argument("fof",help="file or folder to stem")
    parser.add_argument("outfof",help="empty file or folder to write to (typically call this ???-stem)")
    parser.add_argument("--prefixes","--p", help="filename of prefixes, first token of each line")
    parser.add_argument("--suffixes","--s", help="filename of suffixes, first token of each line")
    parser.add_argument("--col",help="which column to change.", type=int, default=5)
    
    args = parser.parse_args()
    
    stem(args.fof, args.prefixes, args.suffixes, args.outfof, args.col)
