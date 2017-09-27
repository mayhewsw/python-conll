#!/home/mayhew2/miniconda3/bin/python
import os,codecs
from collections import defaultdict
from conll.readconll import *
from conll.util import *
import random



def func(folder, outfolder, frac):
    random.seed(1234567)

    fnames = getfnames(folder)

    # this contains the sets of constituents and frequencies
    d = defaultdict(int)

    total = 0
    
    for fname in fnames:
        cdoc = readconll(fname)
        cons = cdoc.getconstituents()
        
        for c in cons:
            d[c.surf()] += 1
            total += 1

    # build the set of names we will keep...
    goal = frac * total
    currnum = 0
    activecons = set()
    
    # impose ordering
    ditems = sorted(d.items())
    # make it random, but consistent.
    random.shuffle(ditems)
    
    for c,freq in ditems:
        activecons.add(c)
        currnum += freq
        if currnum >= goal:
            break

        
    for fname in fnames:
        cdoc = readconll(fname)
        cons = cdoc.getconstituents()

        for con in cons:
            # discard all the names we don't keep. 
            if con.surf() not in activecons:
                #print(con)
                cdoc.removeconstituent(con)

        with open(outfolder + "/" + os.path.basename(fname), "w") as out:
            cdoc.write(out)
                
        
        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("folder",help="")
    parser.add_argument("outfolder",help="")
    parser.add_argument("frac",help="", type=float)

    args = parser.parse_args()
    
    func(args.folder, args.outfolder, args.frac)
