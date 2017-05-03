#!/home/mayhew2/miniconda3/bin/python
import os,codecs,os.path
from collections import defaultdict
from util import getfnames

def func(folder, outfolder, labels=[]):
    fnames = getfnames(folder)

    isfolder = os.path.isdir(folder)
    
    for fname in fnames:
        with open(fname) as f:
            lines = f.readlines()
        outlines = []
        for line in lines:            
            sline = line.split("\t")
            if len(sline) > 5:
                if len(labels) == 0 or sline[0] in labels:            
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
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("folder",help="input file or folder")
    parser.add_argument("outfolder",help="output file or folder")
    parser.add_argument("--labels", help="which labels should we remove? Default will to remove all labels.", default=[], nargs="+")

    args = parser.parse_args()
    
    func(args.folder, args.outfolder, args.labels)
