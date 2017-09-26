#!/home/mayhew2/miniconda3/bin/python
import os,codecs
from collections import defaultdict

def func(folder, outfolder):
    fnames = os.listdir(folder)

    for fname in fnames:
        with open(folder + "/" + fname) as f:
            lines = f.readlines()
        outlines = []
        for line in lines:            
            sline = line.split("\t")
            if len(sline) > 5:            
                # now we will fix sline[5]
                if sline[5].startswith("@"):
                    sline[0] = "B-ORG"
                
            outlines.append("\t".join(sline))
            

        with open(outfolder + "/"+ fname, "w") as out:
            for line in outlines:
                out.write(line);

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("folder",help="")
    parser.add_argument("outfolder",help="")

    args = parser.parse_args()
    
    func(args.folder, args.outfolder)
