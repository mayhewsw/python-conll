#!/home/mayhew2/miniconda3/bin/python
import os,codecs,os.path,math,string
import random
from collections import defaultdict
from conll.util import getfnames, punc, isnum


def uniform():
    """ give each token a uniform weight """
    theta = 0.1
    return theta


def windowed(d):
    # d is distance from nearest entity
    w = 2
    if d > w:
        return 0.0
    else:
        return 1.0


def softwindowed(d):
    theta = 2.0
    return theta * math.exp(-d)


def freq(f):
    """ Weight a token by it's (normalized) frequency """
    theta = 1.0
    return theta*f

def rand():
    """ This randomly includes/excludes elements """
    theta = 0.4
    return 0.0 if random.random() > theta else 1.0


def func(folder, outfolder, mention):
    random.seed(1234567)

    fnames = getfnames(folder)
    isfolder = os.path.isdir(folder)

    # word frequencies.
    wfreq = defaultdict(int)
    weightmass = defaultdict(int)

    # make a first pass to gather word
    # frequencies and distances from entities.
    dists = defaultdict(lambda: defaultdict(int))
    
    # is entity?
    def isent(s):
        return s != "O"

    for fname in fnames:

        # this measures the distance from token i to the nearest
        # named entity

        lastindex = 0

        # boolean for if cond:
        # the previous entity boundary was a sentence
        prevempty = True

        with open(fname) as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            sline = line.split("\t")
            if len(sline) > 5:
                wfreq[sline[5]] += 1

            ent = isent(sline[0])
            empty = len(sline) < 5
            if ent or empty:
                dists[fname][i] = 0
                # when you see this, then go over all tokens since then...
                dd = i - lastindex

                startbias = 0
                endbias = 0

                if empty and prevempty:
                    # these are just large nubmers...
                    startbias = 10000
                    endbias = 10000
                elif empty:
                    endbias = 10000
                elif prevempty:
                    startbias = 10000

                for j in range(lastindex+1, i):
                    disttolast = j - lastindex
                    disttonext = dd - disttolast
                    dists[fname][j] = min(disttolast + startbias, disttonext + endbias)
                lastindex = i
                prevempty = empty


    # normalize the word frequencies
    mx = max(wfreq.values())
    for w in wfreq:
        wfreq[w] /= mx

    for fname in fnames:
        with open(fname) as f:
            lines = f.readlines()
        outlines = []
        for i, line in enumerate(lines):
            
            sline = line.strip().split("\t")
            if len(sline) > 5:

                sline[7] = str(dists[fname][i])

                if (sline[5] in punc or isnum(sline[5])):
                    theta = 1.0
                    sline[6] = 0.0 if random.random() > theta else 1.0
                elif sline[0] == "O":
                    # probability of including
                    #theta = wfreq[sline[5]]
                    theta = 0.01
                    sline[6] = 0.0 if random.random() > theta else 1.0
                    #sline[6] = 0.0
                    #sline[6] = windowed(dists[fname][i])
                    #sline[6] = 1.0
                    #sline[6] = softwindowed(dists[fname][i])
                    #sline[6] = 
                    #sline[6] = rand()
                else:
                    # probabil3y of including
                    theta = 0.3
                    sline[6] = 0.0 if random.random() > theta else 1.0

                weightmass[sline[0]] += sline[6]
                sline[6] = str(sline[6])
                sline[8] = str(wfreq[sline[5]])
                outlines.append("\t".join(sline) + "\n")
            else:
                outlines.append("\n")

        if isfolder:
            fnonly = os.path.basename(fname)
            outpath = outfolder + "/" + fnonly
        else:
            outpath = outfolder

        with open(outpath, "w") as out:
            for line in outlines:
                out.write(line)

    for tag in sorted(weightmass):
        print("{}: {}".format(tag, weightmass[tag]))
    tags = 0
    for k in weightmass:
        if k == "O":
            continue
        tags += weightmass[k]
    print("Final ratio R: {:.2%}".format(tags / sum(weightmass.values())))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Change weights of the file!")

    parser.add_argument("folder", help="input file or folder")
    parser.add_argument("outfolder", help="output file or folder")
    parser.add_argument("--mention", "-m", help="convert to just mention/not mention data", default=False, action="store_true")

    args = parser.parse_args()

    func(args.folder, args.outfolder, args.mention)
