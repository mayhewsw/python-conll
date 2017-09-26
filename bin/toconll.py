#!/usr/bin/python
from __future__ import print_function
from conll.util import getfnames,punc
import codecs,os.path

def convert(fof, outfof=""):
    """ Given a file or folder of text files, this will convert to conll files."""
    
    fnames = getfnames(fof)

    for fname in fnames:    
        with codecs.open(fname,"r", "utf8") as f:
            lines = f.readlines()

        fnonly = os.path.basename(fname)

        outname = os.path.join(outfof, fnonly + ".conll")        
        out = codecs.open(outname, "w", "utf8")
        
        i = 1
        for line in lines:
            #if line[0] == "#":
            #    out.write(line)
            #    continue

            # if you come across an empty line, don't write anything.
            if len(line.strip()) == 0:
                continue

            sline = line.split()
            

            for word in sline:                
                if len(word) == 0:
                    continue
                
                while len(word) > 0 and word[0] in punc:
                    out.write("\t".join(["O", "0", str(i), "x", "x", word[0], "x", "x", "0\n"]))
                    word = word[1:]
                    i += 1

                after = []
                while len(word) > 0 and word[-1] in punc:
                    # insert so the order is correct.
                    after.insert(0, word[-1])
                    word = word[:-1]
                    
                if len(word) > 0:
                    # Now word is pure, unfiltered...
                    out.write("\t".join(["O", "0", str(i), "x", "x", word, "x", "x", "0\n"]))

                    for pn in after:
                        i += 1
                        out.write("\t".join(["O", "0", str(i), "x", "x", pn, "x", "x", "0\n"]))

                i += 1
                
            out.write("\n")


        out.close()

        print("Wrote to: ", outname)
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert an unlabeled text file to conll format. # marks comments which will be ignored. This assumes that text is tokenized by whitespace.")

    parser.add_argument("fof", help="file or folder containing text files.")
    parser.add_argument("--outfof", "-o", help="output file or folder", default="")

    args = parser.parse_args()
    
    convert(args.fof, args.outfof)
    
