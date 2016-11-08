#!/usr/bin/python
import os
from collections import defaultdict

def getstats(dr):
    """
    Given a directory dr containing CoNLL files,
    collect tag and token statistics over the corpus.
    """

    toks = 0
    totaltags = 0
    tags = defaultdict(int)
    
    for fname in os.listdir(dr):
        with open(dr + "/" + fname) as f:
            for line in f:
                if len(line.strip()) == 0: continue
                toks += 1

                tag = line.split("\t")[0]

                if tag != "O":
                    tags[tag] += 1
                    totaltags += 1
                
    print "Tokens: {0}".format(toks)
    print "Total nes: {0}".format(totaltags)
    print "Tag dict:"

    tags = sorted(tags.items())
    
    
    for t,v in tags:
        print t,":",v
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Collect tag statistics from a folder of CoNLL files")

    parser.add_argument("dir",help="")

    args = parser.parse_args()
    
    getstats(args.dir)
