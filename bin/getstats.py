#!/usr/bin/python
import os
from collections import defaultdict
from conll.util import getfnames

def getstats(fof):
    """
    Given a directory dr containing CoNLL files,
    collect tag and token statistics over the corpus.
    """

    if "," in fof:
        fofs = fof.split(",")

        fnames = []
        for f in fofs:
            fnames.extend(getfnames(f))
    else:
        fnames = getfnames(fof)
    
    toks = 0
    totaltags = 0
    totalstarttags = 0
    tags = defaultdict(int)
    
    for fname in fnames:
        with open(fname) as f:
            for line in f:
                if len(line.strip()) == 0: continue
                if "DOCSTART" in line: continue
                toks += 1

                tag = line.strip().split()[0]

                if tag != "O":
                    tags[tag] += 1
                    totaltags += 1
                    if tag[0] == "B":
                        totalstarttags += 1
                
    print("Documents: {0}".format(len(fnames)))
    print("Tokens: {0}".format(toks))
    print("Total nes: {0}".format(totalstarttags))
    print("Total ne tokens: {0}".format(totaltags))
    print("NE percentage: {0}%".format(round(100*totaltags / float(toks), 2)))
    print("Tag dict:")

    tags = sorted(tags.items())
    
    for t,v in tags:
        print(t,":",v)
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Collect tag statistics from a folder of CoNLL files")

    parser.add_argument("dr",help="")

    args = parser.parse_args()
    
    getstats(args.dr)
