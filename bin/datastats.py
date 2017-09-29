#!/usr/bin/python
from collections import defaultdict
from conll.readconll import readconll
from conll import util
from math import sqrt

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

        for f in files:
            cdoc = readconll(f)

            for t in cdoc.tokens:
                tokens[t.s] += 1

            for c in cdoc.getconstituents():
                names[c.label + "\t" + c.surf()] += 1
                tags[c.label] += 1

        namedicts.append(names)
        tokendicts.append(tokens)
        tagdicts.append(tags)

        print("Folder: {}".format(folder))
        print(" Documents: {}".format(len(files)))
        print(" Num tokens: {}".format(sum(tokens.values())))
        print(" Num unique tokens: {}".format(len(tokens.keys())))
        numnames = sum(names.values())
        print(" Num names: {}".format(numnames))
        uniqnames = len(names.keys())
        print(" Num unique names: {}".format(uniqnames))
        print(" Avg num repetitions", numnames / float(uniqnames))
        print(" Unique / Total", uniqnames / float(numnames))
        print(" Tag dict")
        for t in sorted(tags):
            print("  {}: {} ({})"
                  .format(t, tags[t], tags[t] / float(numnames)))

    if len(namedicts) == 2:
        print("Comparison:")

        if tagdicts[0].keys() != tagdicts[1].keys():
            print(" ***Mismatching tag set!***")

        namecos, nameinter, nameweight = cos(namedicts[0], namedicts[1])
        vocabcos, vocabinter, vocabweight = cos(tokendicts[0], tokendicts[1])
        tagcos, taginter, tagweight = cos(tagdicts[0], tagdicts[1])

        print(" Names cos sim: {}".format(namecos))
        print(" Vocab cos sim: {}".format(vocabcos))
        print(" Tag cos sim: {}".format(tagcos))

        numtestnames = sum(namedicts[1].values())
        print(" %names in test seen in training: {}"
              .format(nameweight / float(numtestnames)))
        numtesttokens = sum(tokendicts[1].values())
        print(" %tokens in test seen in training: {}"
              .format(vocabweight / float(numtesttokens)))


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description="Getstats on a directory, or on two directories. If " +
        "there are two directories, they are treated as Train and Test.")

    parser.add_argument("folders", help="Folder(s) to getstats on.", nargs="+")

    args = parser.parse_args()
    getstats(args.folders)
