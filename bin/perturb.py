#!/home/mayhew2/miniconda3/bin/python
import os
import math
from collections import defaultdict
from conll.readconll import readconll
from conll.util import getfnames
from conll.ConllDocument import Constituent
import random


def func(folder, outfolder, precision, recall):
    # This is v1 seed:
    random.seed(1234567)
    # v2 seed:
    #random.seed(4343)

    fnames = getfnames(folder)

    # this contains the sets of constituents and frequencies
    d = defaultdict(int)
    
    namesdocs = []
    total = 0
    labels = list()

    for fname in fnames:
        cdoc = readconll(fname)
        cons = cdoc.getconstituents()

        namesdocs.append((fname,cdoc))
        
        for c in cons:
            d[c.surf()] += 1
            total += 1
            labels.append(c.label)

    labels = list(labels)

    # build the set of names we will keep...
    goal = recall * total
    currnum = 0
    activecons = set()

    # impose ordering
    ditems = sorted(d.items())

    # make it random, but consistent.
    random.shuffle(ditems)

    for c, freq in ditems:
        activecons.add(c)
        currnum += freq
        if currnum >= goal:
            break

    print("Writing to {}".format(outfolder))
    for fname,cdoc in namesdocs:
        cons = cdoc.getconstituents()

        numpos = len(cons)
        for con in cons:
            # discard all the names we don't keep.
            if con.surf() not in activecons:
                # print(con)
                cdoc.removeconstituent(con)
                numpos -= 1

        badspanstoadd = math.ceil(numpos / precision - numpos)
        for _ in range(badspanstoadd):
            start = random.randrange(0, len(cdoc.tokens)-5)
            length = random.randrange(1, 3)
            end = start + length
            randlabel = random.choice(labels)
            newcon = Constituent(randlabel, cdoc.tokens[start:end], (start, end))
            cdoc.addconstituent(newcon)

        with open(outfolder + "/" + os.path.basename(fname), "w") as out:
            cdoc.write(out)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("folder", help="")
    parser.add_argument("outfolder", help="")
    parser.add_argument(
        "--precision",
        "-p",
        help="Set this to the percentage precision (e.g. 0.15)",
        default=1.0,
        type=float)
    parser.add_argument(
        "--recall",
        "-r",
        help="Set this to the percentage recall (e.g. 0.15)",
        default=1.0,
        type=float)

    args = parser.parse_args()

    func(args.folder, args.outfolder, args.precision, args.recall)
