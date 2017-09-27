#!/home/mayhew2/miniconda3/bin/python
import os,codecs,os.path,math,string
from collections import defaultdict
from conll.util import getfnames

def func(folder, outfolder):
    fnames = getfnames(folder)

    isfolder = os.path.isdir(folder)

    wfreq = defaultdict(int)
    weightmass = defaultdict(int)
    
    for fname in fnames:
        with open(fname) as f:
            lines = f.readlines()
        outlines = []
        for line in lines:            
            sline = line.split("\t")
            if len(sline) > 5:
                wfreq[sline[5]] += 1

    mx = max(wfreq.values())
                    
    for fname in fnames:
        with open(fname) as f:
            lines = f.readlines()
        outlines = []
        for i,line in enumerate(lines):

            prevtag = False
            if i > 0:
                prevline = lines[i-1]
                spl = prevline.split("\t")
                prevtag = spl[0][0] == "B" or spl[0][0] == "I"

                    
            nexttag = False
            if i < len(lines)-1:
                nextline = lines[i+1]
                snl = nextline.split("\t")
                nexttag = snl[0][0] == "B" or snl[0][0] == "I"
                
            
            sline = line.split("\t")
            if len(sline) > 5:
                # modify sline[6] to add a weight.

                if prevtag or nexttag:
                    sline[6] = 1.0
                elif sline[5] in string.punctuation:
                    sline[6] = 1.0                
                elif sline[0] == "O":
                    sline[6] = 0.001 #wfreq[sline[5]] / (0.75*float(mx))
                else:
                    sline[6] = 1.0



            weightmass[sline[0]] += sline[6]

            sline[6] = str(sline[6])
            
            outlines.append("\t".join(sline))
            
        if isfolder:
            fnonly = os.path.basename(fname)
            outpath = outfolder + "/"+ fnonly
        else:
            outpath = outfolder
            
        with open(outpath, "w") as out:
            for line in outlines:
                out.write(line);

    print(weightmass)
    total = 0
    for k in weightmass:
        if k == "O":
            continue
        total += weightmass[k]
    print("{}, {}, {}".format(total, weightmass["O"], total / float(weightmass["O"])))
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Change weights of the file!")

    parser.add_argument("folder",help="input file or folder")
    parser.add_argument("outfolder",help="output file or folder")

    args = parser.parse_args()
    
    func(args.folder, args.outfolder)
