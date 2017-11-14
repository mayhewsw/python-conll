#!/usr/bin/python
import os
from collections import defaultdict


def func(folder1, folder2, overwrite=False):
    """ Written from the perspective of the annotation software.
    Old folder is the orig dev folder """
    oldfnames = os.listdir(folder1)
    newfnames = os.listdir(folder2)

    for fname in oldfnames:
        if fname in newfnames:
            print(fname)
            # open them both, compare lines.
            with open(folder1 + "/" + fname) as f:
                oldlines = f.readlines()
            with open(folder2 + "/" + fname) as f:
                newlines = f.readlines()

            while "DOCSTART" in oldlines[0] or len(oldlines[0].strip()) == 0:
                oldlines = oldlines[1:]

            while "DOCSTART" in newlines[0] or len(newlines[0].strip()) == 0:
                newlines = newlines[1:]

            while len(oldlines[-1].strip()) == 0:
                oldlines = oldlines[:-1]

            while len(newlines[-1].strip()) == 0:
                newlines = newlines[:-1]

            if len(oldlines) != len(newlines):
                print("!!! length of files doesn't match. Old:", len(oldlines), " New:", len(newlines))
                # newlines = newlines[:len(oldlines)] ## HAAAAACCCKKKK
                # return

            writelines = []
            for old, new in zip(oldlines, newlines):
                sold = old.split("\t")
                snew = new.split("\t")
                # IMPORTANT! All words from oldline are kept. Just label
                # changed.
                if len(sold) > 5 and len(snew) > 5:  # and sold[0] != snew[0]:

                    # overwrite will copy O labels from new
                    if overwrite:
                        sold[0] = snew[0]
                    else:
                        # otherwise only copy if the new label is not O
                        if snew[0] != "O":
                            sold[0] = snew[0]

                    writelines.append("\t".join(sold))

                    # print sold[5] + "\t" + snew[5]

                else:
                    writelines.append(old)
                    # print("\n")

            with open(folder1 + "/" + fname, "w") as out:
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

    args = parser.parse_args()

    print(args.overwrite)
    func(args.folder1, args.folder2, args.overwrite)
