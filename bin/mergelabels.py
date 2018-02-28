#!/usr/bin/python
import os
from collections import defaultdict
from conll import util

def func(folder1, folder2, overwrite=False, col=0):
    """ Written from the perspective of the annotation software.
    Old folder is the orig dev folder """

    # if folder1 is a folder
    if os.path.isdir(folder1):
        oldfnames = set(os.listdir(folder1))
        newfnames = set(os.listdir(folder2))

        inter = oldfnames.intersection(newfnames)
        print("Old files: {}, new files: {}, intersection: {}".format(len(oldfnames), len(newfnames), len(inter)))

        filepairs = map(lambda p: (os.path.join(folder1, p), os.path.join(folder2, p)), inter)
        
    else:
        # this means folder1 is a file
        filepairs = [(folder1,folder2)]
    
    #efor oldfname,newfname in zip(oldfnames,newfnames):
    # this will loop over a list of fully qualified files and write to new.
    for oldfname,newfname in filepairs:

        with open(os.path.join(oldfname)) as f:
            oldlines = f.readlines()
        with open(os.path.join(newfname)) as f:
            newlines = f.readlines()

        if len(oldlines) != len(newlines):
            print("!!! length of file {} doesn't match:".format(oldfname), len(oldlines), " New:", len(newlines))
            # newlines = newlines[:len(oldlines)] ## HAAAAACCCKKKK
            # return

        # remove empty lines from the end.
        while len(oldlines[-1].strip()) == 0:
            oldlines = oldlines[:-1]

        while len(newlines[-1].strip()) == 0:
            newlines = newlines[:-1]
            
        o = 0
        n = 0
        
        writelines = []
        
        while True:
            if o >= len(oldlines) or n >= len(newlines):
                break
            
            old = oldlines[o]
            new = newlines[n]
            
            while "DOCSTART" in old or len(old.strip()) == 0:
                o += 1
                old = oldlines[o]
                writelines.append("\n")

            while "DOCSTART" in new or len(new.strip()) == 0:
                n += 1
                new = newlines[n]

            o += 1
            n += 1
                
            sold = old.split("\t")
            snew = new.split("\t")
            # IMPORTANT! All words from oldline are kept. Just label
            # changed.
            if len(sold) > 5 and len(snew) > 5:  # and sold[0] != snew[0]:

                # overwrite will copy O labels from new
                if overwrite or col != 0:
                    #mult = 0.004 if sold[0] == "O" else 1.0
                    sold[col] = snew[col]
                else:
                    # otherwise only copy if the new label is not O
                    if snew[0] != "O":
                        sold[0] = snew[0]

                writelines.append("\t".join(sold))

                # print sold[5] + "\t" + snew[5]

            else:
                writelines.append(old)
                # print("\n")

        with open(oldfname, "w") as out:
            for line in writelines:
                out.write(line)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Merge two datasets together. Datasets must be identical in all but labels. Folder 2 will be merged into Folder 1. By default O labels will not be transferred. Use --overwrite option to overwrite O labels.")

    parser.add_argument("folder1", help="merge into here")
    parser.add_argument("folder2", help="merge the files from here")
    parser.add_argument(
        "--overwrite",
        "-o",
        help="overwrite labels?",
        action='store_true')
    parser.add_argument(
        "--column",
        "-c",
        type=int,
        help="which column to merge?",
        default=0)

    
    args = parser.parse_args()

    func(args.folder1, args.folder2, args.overwrite, args.column)
