#!/home/mayhew2/miniconda3/bin/python
import os,codecs,os.path
from collections import defaultdict
from conll.util import getfnames

def wordstart(w, words):
    """ return true if any word in words is a prefix of w """
    for word in words:
        if w.startswith(word):
            return True
    return False

def func(folder, outfolder, labels=[], words=[]):
    fnames = getfnames(folder)

    isfolder = os.path.isdir(folder)

    labdict = {}
    for lab in labels:
        ls= lab.split(":")
        if len(ls) == 1:
            labdict[ls] = "O"
        else:
            labdict[ls[0]] = ls[1]
    
    for fname in fnames:
        with open(fname) as f:
            lines = f.readlines()
        outlines = []
        for line in lines:            
            sline = line.split("\t")
            if len(sline) > 5:
                
                if labels == [] and words == []:
                    sline[0] = "O"
                elif len(labels) > 0 and words == []:
                    if sline[0] in labdict:
                        sline[0] = labdict[sline[0]]
                elif len(labels) == 0 and len(words) > 0:
                    if wordstart(sline[5], words):
                        sline[0] = "O"
                elif len(labels) > 0 and len(words) > 0: 
                    if sline[0] in labdict and wordstart(sline[5], words):
                        sline[0] = "O"
                    
            outlines.append("\t".join(sline))
            
        if isfolder:
            fnonly = os.path.basename(fname)
            outpath = outfolder + "/"+ fnonly
        else:
            outpath = outfolder
            
        with open(outpath, "w") as out:
            for line in outlines:
                out.write(line);

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Modify the labeling of a file, en masse. In the labels list, give this form: oldlabel:newlabel, or just oldlabel, and O will be inferred. ")

    parser.add_argument("folder",help="input file or folder")
    parser.add_argument("outfolder",help="output file or folder")
    parser.add_argument("--labels", help="which labels should we change? Default will to remove all labels.", default=[], nargs="+")
    parser.add_argument("--words", help="which words should have labels removed? Default is no words.", default=[], nargs="+")

    args = parser.parse_args()
    
    func(args.folder, args.outfolder, args.labels, args.words)
