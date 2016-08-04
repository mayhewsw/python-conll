#!/usr/bin/python
import os
from collections import defaultdict
import codecs

def preparesents(folder, outfile):
    """ Reads CoNLL files to create a file to be used for
    language model training. One sentence per line. """
    fnames = os.listdir(folder)

    print "writing sentences to", outfile
    with codecs.open(outfile, "w", "utf-8") as out:
        for fname in fnames:
            with codecs.open(folder + "/" + fname, "r", "utf-8") as f:
                lines = f.readlines()

            currsent = ""
            for line in lines:            
                sline = line.split("\t")
                if len(sline) > 5:            
                    currsent += sline[5] + " "
                else:
                    out.write(currsent.strip() + "\n")
                    currsent = ""


def preparewords(folder, outfile):
    """
    puts all words in one big line. Typically used for
    training a word2vec model

    TODO: consider cleaning punctuation.
    """
    fnames = os.listdir(folder)

    print "writing words to", outfile
    with codecs.open(outfile, "w", "utf-8") as out:    
        for fname in fnames:
            with codecs.open(folder + "/" + fname, "r", "utf-8") as f:
                lines = f.readlines()
            for line in lines:            
                sline = line.split("\t")
                if len(sline) > 5:            
                    out.write(sline[5] + " ")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="")

    parser.add_argument('--words', dest='prepare', action='store_const',
                        const=preparewords, default=preparesents,
                        help='write out words (default: write out sentences)')
    
    parser.add_argument("folder",help="folder containing CoNLL files")
    parser.add_argument("outfile",help="the file to write the text to")

    args = parser.parse_args()
    
    args.prepare(args.folder, args.outfile)
