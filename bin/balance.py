#!/home/mayhew/anaconda3/bin/python
import os,codecs,os.path,math,string
import random
from collections import defaultdict
from conll.util import getfnames, punc, isnum
from numpy.random import choice


def balance(fname, outfname, bstar, weighted):
    """

    :param fname: the input file name. This must have labels (col 0) as well as label confidences (col 6). Alternatively, col 6 can be confidence on O label
    :param outfname: the output file name. Will output weights in column 6.
    :param bstar: the desired balancing value. Usually about 0.15.
    :param weighted: boolean, whether or not this should be weighted. In practice, this means restricting the number of
    O examples included vs including all and giving them scaled weights.
    """
    random.seed(1234567)

    weights = {}
    numpos = 0
    numneg = 0

    with open(fname) as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        sline = line.strip().split("\t")
        if len(sline) > 5 and "DOCSTART" not in line:
            confs = sline[6].strip(",").split(",")
            if len(confs) == 1:
                # assume that the number there is the O confidence. 
                oweight = float(sline[6])
            else:
                scorelist = list(map(lambda p: p.split(":"), sline[6].strip(",").split(",")))
                scoredict = dict(scorelist)
                oweight = float(scoredict["O"])

            if sline[0] == "O":
                # don't allow negative weights...
                weights[i] = max(0, oweight)
                numneg += 1
            else:
                weights[i] = oweight
                numpos += 1

    total = sum(weights.values())
    totalmass = (1-bstar) * numpos / bstar

    print(totalmass)

    print(weighted)

    if bstar < 0:
        # I don't care if weighted or not.
        # set all weights to 1, as long as oweight > 0 (those are positives.)
        for i in weights:
            if weights[i] > 0:
                weights[i] = 1.0

    elif weighted:
        for i in weights:
            weights[i] = totalmass * weights[i] / total
    else:
        sweighted = sorted(weights.items(), key=lambda p: p[1], reverse=True)
        # largest weights are at the top.

        numneg = (numpos - bstar*numpos) / bstar

        numadded = 0
        for i, weight in sweighted:
            if numadded < numneg:
                weights[i] = 1.0
            else:
                weights[i] = 0.0

            numadded += 1

    outlines = []
    for i, line in enumerate(lines):
        sline = line.strip().split("\t")
        if len(sline) > 5 and "DOCSTART" not in line:
            if sline[0] == "O":
                # this O gets this weight.
                oweight = weights[i]
                sline[6] = oweight  # if i in negs else 0.0
            else:
                # Mention tokens stay the same.

                # If a mention token is predicted as being an O, make that happen.
                if weights[i] > 0:
                    sline[0] = "O"
                    sline[6] = weights[i]
                else:
                    sline[6] = 1.0

            sline[6] = str(sline[6])
            outlines.append("\t".join(sline) + "\n")
        else:
            outlines.append("\n")

    print("Writing to", outfname)
    with open(outfname, "w") as out:
        for line in outlines:
            out.write(line)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="This takes a conll file of predictions+confidences, "
                                                 "and reweights the O tokens so the overall b is 0.15")

    parser.add_argument("folder", help="input file or folder")
    parser.add_argument("outfolder", help="output file or folder")
    parser.add_argument("bstar", help="Gold standard balance ratio. 0<b<1. Usually this is about 0.15.", type=float)
    parser.add_argument("--weighted", help="whether this should be run weighted or not.", action="store_true", default=False)

    args = parser.parse_args()

    balance(args.folder, args.outfolder, args.bstar, args.weighted)

