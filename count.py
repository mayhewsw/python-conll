#!/home/mayhew2/miniconda3/bin/python
import os,codecs
from collections import defaultdict

## Count unique tokens in a conll folder.

def func(folder):
    fnames = os.listdir(folder)

    tokens = defaultdict(int)
    chars = defaultdict(int)
    total = 0
    
    for fname in fnames:
        with open(folder + "/" + fname) as f:
            lines = f.readlines()
        outlines = []
        for line in lines:            
            sline = line.split("\t")
            if len(sline) > 5:            
                # now we will fix sline[5]
                tokens[sline[5]] += 1
                for c in list(sline[5]):
                    chars[c] += 1
                total += 1
                
    print("out of", total, "tokens")
    print("there are", len(tokens), "unique tokens")
    print("unique over total: ", len(tokens) / float(total))

    chars = list(filter(lambda p: p[1] > 100, chars.items()))
    
    print("alphabet size is:", len(chars))
    for c in chars:
        print(c, end=",")
    print()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("folder",help="")

    args = parser.parse_args()
    
    func(args.folder)
