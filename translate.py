#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import codecs
from collections import defaultdict
from collections import deque
import util

def translate(folder, outfolder, flist):
    """
    Translate by word a bunch of CoNLL files found in folder, and write the out to outfolder. Use the files in flist
    as the word mappings.
    
    folder -- a folder containing CoNLL files to be translated
    outfolder -- where the translated files will go
    flist -- a list of files containing word mappings, each of the format: source \t target. Order this list by trustworthiness from most to least.
    """
    
    fnames = os.listdir(folder)

    # this maps source word to [best target, next target, next target...]
    wordmap = defaultdict(list)

    # map punctuation so we have a good idea of how much is translated.
    # TODO: consider not counting punctuation.
    punc = list(u"<>/?:;()`~!@#$%^&*-_=+|[]{}.,»")
    otherpunc = ["...",u'",',u"”,",u"”.",u"»,",u"»."]
    for p in punc.extend(otherpunc):
        wordmap[p].append(p)

    # be sure to order files in flist according to trustworthiness, most to least.
    # that is, if a word has multiple translations, the first is the best.
    # TODO: include scores in wordmap also
    for fname in flist:
        with codecs.open(fname,"r","utf-8") as f:
            lines = f.readlines()
            for line in lines:
                sline = line.strip().split("\t")            
                if len(sline) > 1:
                    wordmap[sline[0]].append(sline[1])

    fixed = 0
    total = 0
    unfixed = defaultdict(int)
    for fname in fnames:
        print fname
        with codecs.open(folder + "/" + fname, "r", "utf-8") as f:
            lines = f.readlines()
        outlines = []
        queue = deque()
        for line in lines:            
            sline = line.split("\t")
            if len(sline) > 5:
                total += 1
                sline[5] = sline[5].lower()
                      
                if sline[5] in wordmap:
                    fixed += 1
                    choices = wordmap[sline[5]]

                    # select the current word according to a language model
                    # conditioned on prior 2 words.
                    # TODO: add as an option
                    if len(choices) > 1 and len(queue) == 2:
                        ngramlist = []
                        for c in choices:
                            ngramlist.append(" ".join(queue) + " " + c + "\n")
                        
                        result = util.call_lm(ngramlist)
                        bestline = result.split("\n")[0]
                        sline[5] = bestline.split()[-1].decode("utf8")
                    else:
                        # choose the first one
                        sline[5] = choices[0]
                else:
                    unfixed[sline[5]] += 1

                queue.append(sline[5])
                if len(queue) > 2:
                    queue.popleft()                   
                
            else:
                queue = deque()
                    
            outlines.append("\t".join(sline))
            

        with codecs.open(outfolder + "/"+ fname, "w","utf-8") as out:
            for line in outlines:
                out.write(line);
                
    print "Translated {0} of the words".format(fixed / float(total))

    print "Wordmap size:", len(wordmap)

    totallen = 0
    for w in wordmap:
        if len(wordmap[w]) > 1:
            print w, wordmap[w]
        totallen += len(wordmap[w])

    print "Average num entries: ", totallen / float(len(wordmap))
    
    for m in util.<sortmap(unfixed, k = 5):
        print m[0], m[1]
    
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="This translates a file into another language")

    parser.add_argument("folder",help="")
    parser.add_argument("outfolder",help="")

    args = parser.parse_args()
    
    translate(args.folder, args.outfolder)



