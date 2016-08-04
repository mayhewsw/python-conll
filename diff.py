#!/usr/bin/python
import os

def diff(oldfolder, newfolder):
    """ Written from the perspective of the annotation software.
    Old folder is the orig dev folder """
    oldfnames = os.listdir(oldfolder)
    newfnames = os.listdir(newfolder)

    for fname in oldfnames:
        if fname in newfnames:
            print fname
            # open them both, compare lines.            
            with open(oldfolder + "/" + fname) as f:
                oldlines = f.readlines()
            with open(newfolder + "/" + fname) as f:
                newlines = f.readlines()

            if len(oldlines) != len(newlines):
                print "What.... length of files doesn't match. Old:",len(oldlines)," New:",len(newlines)
                return
                
            for old,new in zip(oldlines, newlines):
                sold = old.split("\t")
                snew = new.split("\t")
                if len(sold) > 5 and len(snew) > 5 and sold[0] != snew[0]:
                    print sold[5],sold[0],snew[0]

            print
                       
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="", usage="Use this script to compare folders. These folders must contain exact duplicates of conll files, but with different labels. Intended to be used in tandem with the ner-annotation tool, as a way to merge annotations back into the originals.")

    parser.add_argument("oldfolder",help="original folder")
    parser.add_argument("newfolder",help="modified version of original folder")

    args = parser.parse_args()
    
    diff(args.oldfolder, args.newfolder)
