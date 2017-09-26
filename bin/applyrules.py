#!/home/mayhew2/miniconda3/bin/python
import os,codecs
from conll.readconll import readconll
from collections import defaultdict

def func(folder, outfolder, ruleslist):
    fnames = os.listdir(folder)

    with open(ruleslist) as f:
        rules = list(map(lambda l: l.strip().split("\t"), f.readlines()))

    counts = defaultdict(int)

    i= 0
        
    for fname in fnames:
        print(fname)
        i += 1
        cdoc = readconll(folder + "/" + fname)

        for r in rules:
            label = r[1]
            entity = r[0]
            matches = cdoc.findmatches(entity)
            
            if len(matches) > 0:
                counts[entity+":"+label] += len(matches)

        #if i > 10:
        #    break
            

    print(counts)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("folder",help="")
    parser.add_argument("outfolder",help="")
    parser.add_argument("ruleslist",help="")

    args = parser.parse_args()
    
    func(args.folder, args.outfolder, args.ruleslist)
