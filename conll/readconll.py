#!/home/mayhew2/miniconda3/bin/python
import os,codecs
from collections import defaultdict
from .ConllDocument import *


    

def readconll(fname):
    """ This reads a conll file into a conlldocument """
    
    with open(fname) as f:
        lines = f.readlines()

    return readconll_fromlines(lines)


def readconll_fromlines(lines):
    
    #List<IntPair> spans = new ArrayList<>();
    spans = []

    #List<String> labels = new ArrayList<>();
    labels = []

    #List<Integer> sentenceEndPositions = new ArrayList<>();
    sentenceEndPositions = []
    tokens = []
    start = -1
    label = ""

    i = 0
    for  line in lines:
        sline = line.split("\t")

        if line.startswith("B-") or line.startswith("U-"):
            # two consecutive entities.
            if start > -1:
                # peel off a constituent if it exists.
                spans.append((start, i))
                labels.append(label)

            start = i
            label = sline[0].split("-")[1];

        elif sline[0].startswith("I-"):
            # don't do anything....
            pass
        else:
            # this is a sentence boundary.
            if len(line.strip()) == 0:
                # perhaps this is i+1?
                # in case there are multiple empty lines at the end.
                if (i not in sentenceEndPositions and i > 0):
                    sentenceEndPositions.append(i)

            # it's O or it's empty
            if start > -1:
                # peel off a constituent if it exists.
                spans.append((start, i))
                labels.append(label)

            label = "";
            start = -1;

        # add the word form to the sentence.
        if len(sline) > 5 and sline[5] != "-DOCSTART-" and len(sline[5].strip()) > 0:
            tokens.append(Token(sline[2],sline[3],sline[5]))
            i += 1

    # in case the very last line is an NE.
    if start > -1:
        spans.append((start, i));
        labels.append(label);

    # in case there are no empty lines.
    if i not in sentenceEndPositions: 
        sentenceEndPositions.append(i)


    constituents = []
    for label,span in zip(labels,spans):
        c = Constituent(label, tokens[span[0]:span[1]], span)
        constituents.append(c)

    cdoc = ConllDocument(tokens, constituents)
    return cdoc
