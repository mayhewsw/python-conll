#!/usr/bin/python
from __future__ import print_function
import os
from collections import defaultdict
import codecs

def func(folder1, folder2, endingsfname):
    """ Written from the perspective of the annotation software.
    Old folder is the orig dev folder """
    oldfnames = os.listdir(folder1)
    newfnames = os.listdir(folder2)

    with codecs.open(endingsfname) as f:
        line = f.read()
        endings = line.split()

    e2w = defaultdict(list)
    
    for fname in oldfnames:
        if fname in newfnames:
            # open them both, compare lines.            
            with codecs.open(folder1 + "/" + fname, "r", "utf8") as f:
                oldlines = f.readlines()
            with codecs.open(folder2 + "/" + fname, "r", "utf8") as f:
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
                print("!!! length of files doesn't match. Old:",len(oldlines)," New:",len(newlines))
                #newlines = newlines[:len(oldlines)] ## HAAAAACCCKKKK
                return
                
            for old,new in zip(oldlines, newlines):
                sold = old.split("\t")
                snew = new.split("\t")
                # IMPORTANT! All words from oldline are kept. Just label changed.
                if len(sold) > 5 and len(snew) > 5: # and sold[0] != snew[0]:
                    # this needs to be commented.
                    origword = sold[5] # orig
                    romanword = snew[5]  # uly
                    
                    for e in endings:
                        if romanword.endswith(e):
                            e2w[e].append(origword)

    outlist = []
    for e in e2w:
        words = e2w[e]

        if len(words) < 3:
            continue

        #print(e + " with " + str(len(words)) + " words")
        # find common endings in words
        # get shortest word
        shortest = sorted(words, key=len)[0]
        i = len(shortest)

        single = set()
        while True:
            for w in words:
                affix = w[-i:]
                single.add(affix)
                
            if len(single) > 1:
                i -= 1
                single = set()
            else:
                break
        ending = list(single)[0]

        
        # force all endings to have at least two characters.
        if len(ending) > 2:
            print(e + " : " + ending.encode("utf8"))
            outlist.append(ending)
        else:
            print(e + " : no ending")
            
    with codecs.open(endingsfname + ".orig", "w", "utf8") as out:
        outlist = sorted(outlist, key=len, reverse=True)
        out.write(u" ".join(outlist))
        
        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("orig",help="orig script")
    parser.add_argument("romanized",help="romanized script")
    parser.add_argument("endingsfname",help="merge the files from here")

    args = parser.parse_args()
    
    func(args.orig, args.romanized, args.endingsfname)
