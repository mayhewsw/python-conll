#!/usr/bin/python
import os
from collections import defaultdict
import codecs
from conll import util


def densify(fof, outfof, window=-1):
    """ Given a file, this will densify the file. That is, keep only tokens
    within a window of labels. By default (window=-1), this does nothing."""

    fnames = util.getfnames(fof)
    isdir = os.path.isdir(fof)

    for fname in fnames:

        outlines = set()
        i = 0
        
        with codecs.open(fname, "r", "utf8") as f:
            lines = f.readlines()

        if window == -1:
            outwrite = lines
            containscontent = True
        else:
            for line in lines:
                sline = line.split("\t")
                if len(sline) > 5:
                    tag = sline[0]
                    if tag != "O":
                        # this is a label.
                        # add w before and w after.
                        # don't even need to worry about range checking!
                        for j in range(i, i-window-1, -1):
                            if len(lines[j].strip()) == 0:
                                break
                            outlines.add(j)


                        for j in range(i, i+window+1):
                            if len(lines[j].strip()) == 0:
                                break
                            outlines.add(j)
                else:
                    outlines.add(i)

                i += 1

            # conflate empty lines.
            outwrite = []
            lastlinewasempty = False
            containscontent = False
            for i,line in enumerate(lines):
                if i in outlines:
                    isempty = len(line.strip()) == 0
                    if isempty:
                        if not lastlinewasempty:
                            lastlinewasempty = True
                            outwrite.append(line);
                    else:
                        containscontent = True
                        outwrite.append(line);
                        lastlinewasempty = False

        if isdir:
            outfname = outfof + "/" + os.path.basename(fname)
        else:
            outfname = outfof
                    
        # if outlines isn't empty...
        if containscontent:
            with codecs.open(outfname , "w", "utf8") as out:
                for line in outwrite:
                    out.write(line)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="This will densify a conll file. With no options, it does nothing. If you want to remove all sentences with no tags, run with window=<very large number>")

    parser.add_argument("fof",help="Input file or folder")
    parser.add_argument("outfof",help="Output file or folder")
    parser.add_argument("--window", "-w",help="Window", type=int, default=-1)

    args = parser.parse_args()
    
    densify(args.fof, args.outfof, args.window)
