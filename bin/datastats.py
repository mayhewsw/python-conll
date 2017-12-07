#!/usr/bin/python
from collections import defaultdict
from conll.readconll import readconll
from conll import util
from math import sqrt, log

"""
desired functions:
single folder: return
* number documents
* number sentences
* number of tokens
* number of named entities
* number unique named entities
* number unique contexts

two folders: return
* number documents in common
* number sentences in common
* number tokens in common
* number of named entities in common
* number of unique named entities in common
* number of contexts in common

"""


def cos(d1, d2):
    inter = set(d1.keys()).intersection(set(d2.keys()))

    weightedinter = 0
    num = 0
    den1 = 0
    den2 = 0
    for t in inter:
        weightedinter += min(d1[t], d2[t])
        num += d1[t] * d2[t]
        den1 += d1[t]**2
        den2 += d2[t]**2

    return num / (sqrt(den1)*sqrt(den2)), len(inter), weightedinter

def norm(d):
    denom = sum(d.values())
    for k in d:
        d[k] = d[k] / float(denom)
    return d

def KL(d1, d2):
    # augment counts of d1, so
    # every token in d2 is accounted for.
    for k in d2:
        d1[k] += 1
    
    d1 = norm(d1)
    d2 = norm(d2)
    
    inter = set(d1.keys()).intersection(set(d2.keys()))
    total = 0
    for t in inter:
        total += d1[t] * log( d1[t] / d2[t])

    return total, len(inter)
        


def getstats(folders):
    if len(folders) > 2:
        print(">2 folders is not supported. Will only operate on {} and {}"
              .format(folders[0], folders[1]))

    # this will only ever have two elements
    namedicts = []
    tokendicts = []
    tagdicts = []

    for folder in folders:
        files = util.getfnames(folder)
        names = defaultdict(int)
        tags = defaultdict(int)
        tokens = defaultdict(int)
        weights = 0
        nametokens = 0
        sentences = 0

        for f in files:
            cdoc = readconll(f)

            sentences += len(cdoc.sentenceends)

            for t in cdoc.tokens:
                if t.weight > 0:
                    tokens[t.s] += t.weight
                weights += t.weight

            for c in cdoc.getconstituents():
                # assume that all tokens in a constituent share the same weight.
                for t in c.tokens:
                    if t.weight > 0:
                        nametokens += t.weight
                        names[c.label + "\t" + c.surf()] += t.weight
                        tags[c.label] += t.weight

        namedicts.append(names)
        tokendicts.append(tokens)
        tagdicts.append(tags)

        numtokens = sum(tokens.values())
        numnames = sum(names.values())
        uniqnames = len(names.keys())

        try:
            reps = numnames / float(uniqnames)
            uniqs = uniqnames / float(numnames)
            tagpercentage = nametokens / numtokens
            weightedtagpercentage = nametokens / weights
        except ZeroDivisionError:
            reps = 0.0
            uniqs = 0.0
            tagpercentage = 0.
            weightedtagpercentage = 0.

        print("{}: {}".format("Folder", folder))
        print(" {:<20}{:>10}".format("Documents", len(files)))
        print(" {:<20}{:>10,}".format("Num tokens", numtokens))
        print(" {:<20}{:>10,}".format("Num unique tokens", len(tokens.keys())))
        print(" {:<20}{:>10,}".format("Num sentences", sentences))
        print(" {:<20}{:>10,}".format("Num names", numnames))
        print(" {:<20}{:>10,}".format("Num name tokens", nametokens))
        print(" {:<20}{:>10,}".format("Num unique name tokens", uniqnames))
        print(" {:<20}{:>10.2}".format("Avg num repetitions", reps))
        print(" {:<20}{:>10.2}".format("Unique / total", uniqs))
        print(" {:<20}{:>10.2%}".format("Tag %", tagpercentage))
        print(" {:<20}{:>10.2%}".format("Weighted Tag %", weightedtagpercentage))
        print(" Tag dict")
        for t in sorted(tags):
            print("  {}: {} ({:.2%})"
                  .format(t, tags[t], tags[t] / float(numnames)))

    if len(namedicts) == 2:
        print("Comparison:")

        if tagdicts[0].keys() != tagdicts[1].keys():
            print(" ***Mismatching tag set!***")

        namecos, nameinter, nameweight = cos(namedicts[0], namedicts[1])
        vocabcos, vocabinter, vocabweight = cos(tokendicts[0], tokendicts[1])
        vocabkl, inter  = KL(tokendicts[0], tokendicts[1])
        tagcos, taginter, tagweight = cos(tagdicts[0], tagdicts[1])

        print(" Names cos sim: {}".format(namecos))
        print(" Vocab cos sim: {}".format(vocabcos))
        print(" Vocab overlap: {}".format(vocabinter))
        print(" Vocab KL divg: {}".format(vocabkl))
        print(" Tag cos sim: {}".format(tagcos))

        numtestnames = sum(namedicts[1].values())
        print(" %names in test seen in training: {}"
              .format(nameinter / float(numtestnames)))
        
        numtesttokens = sum(tokendicts[1].values())
        print(" %tokens in test seen in training: {}"
              .format(vocabinter / float(numtesttokens)))


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description="Getstats on a directory, or on two directories. If " +
        "there are two directories, they are treated as Train and Test.")

    parser.add_argument("folders", help="Folder(s) to getstats on.", nargs="+")

    args = parser.parse_args()
    getstats(args.folders)
