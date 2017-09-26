#!/usr/bin/python
import os
from collections import defaultdict

def compare(folder, folder2, diff):
    """Given two folders of ConLL files, this compares matching
    files and prints all lines that disagree on the label.
    """
    fnames = sorted(os.listdir(folder))

    # this counts disagreements in labels between
    # folders (thanks stackoverflow)
    confmat = defaultdict(lambda : defaultdict(int))
    
    for fname in fnames:
        if diff: print fname
        try:
            with open(folder + "/" + fname) as f:
                lines = f.readlines()

            with open(folder2 + "/" + fname) as f:
                lines2 = f.readlines()
        except IOError as e:
            print e
            continue

        while "-DOCSTART-" in lines[0] or lines[0].strip() == "":
            lines = lines[1:]

        while "-DOCSTART-" in lines2[0] or lines2[0].strip() == "":
            lines2 = lines2[1:]
            
        for line,line2 in zip(lines, lines2): 
            sline = line.split("\t")
            sline2 = line2.split("\t")

            if len(sline) < 5:            
                continue

            if len(sline2) < 5:
                print "line2 is shorter than line1..."
                print line,line2
                exit()
            
            if sline[5] != sline2[5]:
                #print fname
                #print line, line2
                #print "words don't match between lines"
                #exit()
                pass

            if sline[0] != sline2[0] and diff:
                print sline[5] + "\t" + sline[0] + "\t" + sline2[0]

            confmat[sline[0]][sline2[0]] += 1
        if diff: print

    confkeys = sorted(confmat.keys())


    fmt ="{0:>6}"
    print
    
    # print header first
    for key in [""] + confkeys:
        print fmt.format(key),
    print

    # print confmat
    for key in confkeys:
        print fmt.format(key),
        for key2 in confkeys:
            print fmt.format(confmat[key][key2]),
        print


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("folder",help="Original folder of CoNLL files")
    parser.add_argument("folder2",help="Newly labeled version of original folder")
    parser.add_argument("--diff", default=False, action="store_true")
    
    args = parser.parse_args()
    
    compare(args.folder, args.folder2, args.diff)
