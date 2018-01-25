#!/home/mayhew2/miniconda3/bin/python
import os,codecs,os.path,math,string
import random
from collections import defaultdict
from conll.util import getfnames, punc, isnum

def uniform():
    """ give each token a uniform weight """
    theta = 0.2
    return theta

def window(d):
    # d is distance from nearest entity
    w = 1
    if d > w:
        return 0.0
    else:
        return 1.0

def softwindow(d):
    theta = 1.0
    return theta * math.exp(-d)

def freq(f):
    """ Weight a token by it's (normalized) frequency """
    theta = 1.0
    return theta*f


def func(folder, outfolder, mention, methods):
    """ methods is a list. Can contain: punc, window, softwindow, frequency, uniform """
    
    random.seed(1234567)

    uselearned = True
    
    fnames = getfnames(folder)
    isfolder = os.path.isdir(folder)

    # word frequencies.
    wfreq = defaultdict(int)
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

                if mention:
                    # in this case, we don't want weights.
                    sline[6] = 1.0
                    if sline[0] != "O":
                        sline[0] = "B-MNT"
                elif sline[0] == "O":

                    # These all give weights to all methods.
                    if "softwindow" in methods:
                        sline[6] = softwindow(dists[fname][i])
                        
                    if "freq" in methods:
                        sline[6] = freq(wfreq[sline[5]])
                        
                    if "uniform" in methods:
                        sline[6] = uniform()

                    # The following give weights to just a few.
                    if "punc" in methods:
                        if sline[5] in punc or isnum(sline[5]):
                            sline[6] = 1.0

                    if "window" in methods:
                        if dists[fname][i] <= 1:
                            sline[6] = 1.0
                        
                    if sline[6] == "x":
                        sline[6] = 0.0
                else:
                    sline[6] = 1.0

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

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Change weights of the file!")

    parser.add_argument("folder", help="input file or folder")
    parser.add_argument("outfolder", help="output file or folder")
    parser.add_argument("--mention", "-m", help="convert to just mention/not mention data", default=False, action="store_true")
    parser.add_argument("--methods", help="comma separated list of methods", default="")

    args = parser.parse_args()
    func(args.folder, args.outfolder, args.mention, args.methods.split(","))
