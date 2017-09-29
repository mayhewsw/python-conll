#!/usr/bin/python
import math
from collections import defaultdict
from conll.readconll import readconll
from conll import util

# this will take one (train) or two directories (train, test) and print
# comparison stats, as well as individual stats (this should probably be
# folded into the getstats.py script)

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


def getstats(folders):
    if len(folders) > 2:
        print(">2 folders is not supported. Will only operate on {} and {}"
              .format(folders[0], folders[1]))

    # this will only ever have two elements
    namedicts = []

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
            print("  {}: {} ({})".format(t, tags[t], tags[t] / float(numnames)))

    if len(namedicts) == 2:
        n1 = namedicts[0]
        n2 = namedicts[1]
        inter = set(n1.keys()).intersection(set(n2.keys()))

        weightedinter = 0
        for n in inter:
            weightedinter += min(n1[n], n2[n])

        print("Names in common: {}".format(weightedinter))
        print("Unique names in common: {}".format(len(inter)))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Getstats on a directory, or on two directories.")

    parser.add_argument("folders", help="Folder(s) to getstats on.", nargs="+")

    args = parser.parse_args()
    getstats(args.folders)
