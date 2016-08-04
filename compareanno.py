#!/usr/bin/python
import os
from collections import defaultdict

def compare(folder, folder2):
    """Given two folders of ConLL files, this compares matching
    files and prints all lines that disagree on the label.
    """
    fnames = sorted(os.listdir(folder))

    # this will count labels as if they were merged
    # when there are no disagreements
    tags = defaultdict(int)

    # this counts disagreements in labels between
    # folders
    disagree = defaultdict(int)
    
    for fname in fnames:

        try:
            with open(folder + "/" + fname) as f:
                lines = f.readlines()

            with open(folder2 + "/" + fname) as f:
                lines2 = f.readlines()
        except Exception as e:
            print "Whoops! trying again..."
            continue

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
                print fname
                print line, line2
                print "words don't match between lines"

            l = sline[0] + " : " + sline[5] + ", " + sline2[0] + " : " + sline2[5]
                
            if sline[0] == "O" and sline2[0] == "O":
                pass            
            elif sline[0] == "O" and sline2[0] != "O":
                tags[sline2[0]] += 1
                print l
            elif sline[0] != "O" and sline2[0] == "O":
                tags[sline[0]] += 1
                print l
            elif sline[0] != sline2[0]:
                disagree[sline[0] + ":" + sline2[0]] += 1
                print l
            else:
                tags[sline[0]] += 1

    tags = sorted(tags.items())

    print "tags"
    for t,v in tags:
        print t,":",v

    disagree = sorted(disagree.items())

    print
    print "disagree"
    for t,v in disagree:
        print t,":",v


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("folder",help="")
    parser.add_argument("folder2",help="")

    args = parser.parse_args()
    
    compare(args.folder, args.folder2)
