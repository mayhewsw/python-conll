#!/home/mayhew2/miniconda3/bin/python
from .ConllDocument import Token, Constituent, ConllDocument


def readconll(fname):
    """ This reads a conll file into a conlldocument """

    with open(fname) as f:
        lines = f.readlines()

    return readconll_fromlines(lines)


def readconll_fromlines(lines):

    spans = set()
    labels = set()

    sentenceEndPositions = []
    
    # tokens contains pairs: (tokenindex, tokenobject)
    tokens = set()
    start = -1
    label = ""

    # i represents the token index.
    i = 0
    for line in lines:
        sline = line.split("\t")

        if line.startswith("B-") or line.startswith("U-"):
            # two consecutive entities.
            if start > -1:
                # peel off a constituent if it exists.
                spans.add((start, i))
                labels.add((label, i))
                
            start = i
            label = sline[0].split("-")[1]

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
                spans.add((start, i))
                labels.add((label, i))

            label = ""
            start = -1

        # add the word form to the sentence.
        if len(sline) > 5 and sline[5] != "-DOCSTART-" and len(sline[5].strip()) > 0:
            tokens.add((i, Token(sline[2], sline[3], sline[5], sline[6])))
            i += 1

    # in case the very last line is an NE.
    if start > -1:
        spans.add((start, i))
        labels.add((label, i))

    # Convert sets to lists.
    spans = sorted(spans, key=lambda p: p[1])
    labels = map(lambda p: p[0], sorted(labels, key=lambda p: p[1]))

    tokens = list(map(lambda p: p[1], sorted(tokens, key=lambda p: p[0])))
    
    #print(spans)
    #print(list(labels))
    
    # in case there are no empty lines.
    if i not in sentenceEndPositions:
        sentenceEndPositions.append(i)

    constituents = []
    for label, span in zip(labels, spans):
        c = Constituent(label, tokens[span[0]:span[1]], span)
        constituents.append(c)

    cdoc = ConllDocument(tokens, constituents, sentenceEndPositions)
    return cdoc
