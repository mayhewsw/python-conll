#!/usr/bin/python

#!/usr/bin/python
import os
from collections import defaultdict
import codecs
from conll import util
import random


def dense2(fof, outfof):
    fnames = util.getfnames(fof)
    isdir = os.path.isdir(fof)
    random.seed(1234567)

    for fname in fnames:

        outlines = []
        with codecs.open(fname, "r", "utf8") as f:
            lines = f.readlines()

        for line in lines:
            sline = line.split("\t")
            if len(sline) > 5:
                tag = sline[0]
                if tag == "O":
                    # maybe add, maybe don't
                    if random.random() < 0.02:
                        outlines.append(line)
                    else:
                        outlines.append("\n")
                    
                else:
                    outlines.append(line)
            else:
                outlines.append(line)

        if isdir:
            outfname = outfof + "/" + os.path.basename(fname)
        else:
            outfname = outfof
        # if outlines isn't empty...
        with codecs.open(outfname, "w", "utf8") as out:
            for line in outlines:
                out.write(line)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("fof",help="Input file or folder")
    parser.add_argument("outfof",help="Output file or folder")

    args = parser.parse_args()
    
    dense2(args.fof, args.outfof)
