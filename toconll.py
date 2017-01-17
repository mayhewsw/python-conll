#!/usr/bin/python
from __future__ import print_function

def convert(fname):
    with open(fname) as f:
        lines = f.readlines()

    out = open(fname + ".conll", "w")
    i = 0
    for line in lines:
        if len(line.strip()) == 0:
            i = 0
            out.write("\n")
            continue
        
        sline = line.split()

        for word in sline:
            out.write("\t".join(["O", "0", str(i), "x", "x", word, "x", "x", "0\n"]))
        out.write("\n")
        
        i += 1
    out.close()
    
    print("Wrote to: ", fname + ".conll")
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert an unlabeled text file to conll format. # marks comments which will be ignored. This assumes that
    text is tokenized by whitespace.")

    parser.add_argument("file", help="input file to be converted.")

    args = parser.parse_args()
    
    convert(args.file)
