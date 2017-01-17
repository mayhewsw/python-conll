#!/usr/bin/python
import os
from collections import defaultdict
import codecs
from util import getfnames

def preparesents(fof, outfile):
    """ Reads CoNLL files to create a file to be used for
    language model training. One sentence per line. """

    fnames = getfnames(fof)
    
    print "writing sentences to", outfile
    with codecs.open(outfile, "w", "utf-8") as out:
        for fname in fnames:
            with codecs.open(fname, "r", "utf-8") as f:
                lines = f.readlines()

            currsent = ""
            for line in lines:            
                sline = line.split("\t")
                if len(sline) > 5:            
                    currsent += sline[5] + " "
                else:
                    out.write(currsent.strip() + "\n")
                    currsent = ""


def preparewords(fof, outfile):
    """
    puts all words in one big line. Typically used for
    training a word2vec model

    TODO: consider cleaning punctuation.
    """

    fnames = getfnames(fof)
    
    print "writing words to", outfile
    with codecs.open(outfile, "w", "utf-8") as out:    
        for fname in fnames:
            with codecs.open(fname, "r", "utf-8") as f:
                lines = f.readlines()
            for line in lines:            
                sline = line.split("\t")
                if len(sline) > 5:            
                    out.write(sline[5] + " ")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert conll files into different formats -- either all into one line, or separate sentences per line.")

    parser.add_argument('--words', dest='prepare', action='store_const',
                        const=preparewords, default=preparesents,
                        help='write out words (default: write out sentences)')

    # fof: file or folder
    parser.add_argument("fof",help="file or folder containing CoNLL files")
    parser.add_argument("outfile",help="the file to write the text to")

    args = parser.parse_args()
    
    args.prepare(args.fof, args.outfile)
