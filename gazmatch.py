#! /home/mayhew2/miniconda3/bin/python
import os,codecs
from collections import defaultdict

## This file counts the number of times any token matches
# any token in a gazetteer file.



def func(folder, gazfile):
    fnames = os.listdir(folder)

    gaz = set()
    with codecs.open(gazfile, "r", "utf8") as f:
        for line in f:
            for tok in line.strip().split():
                gaz.add(tok)

    print("# gaz entries:", len(gaz))
    
    match = 0
    toks = 0
    for fname in fnames:
        with codecs.open(folder + "/" + fname, "r", "utf8") as f:
            lines = f.readlines()

        for line in lines:            
            sline = line.split("\t")
            if len(sline) > 5:            
                # now we will fix sline[5]
                toks += 1
                if sline[5] in gaz:
                    match += 1

    print("# num toks", toks)
    print("# num gaz matches", match)
    

    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("folder",help="")
    parser.add_argument("gazfile",help="")

    args = parser.parse_args()
    
    func(args.folder, args.gazfile)
