#!/usr/bin/python
import os
from collections import defaultdict
import codecs

def striptowindow(lines, window):
    """ takes a list of lines and only keeps words within a window of each tag. """
    outlines = []

    # keep window in memory
    # when you see a name, add saved window from behind
    # add window before

    wlines = []
    end = -1
    
    for i,line in enumerate(lines):

        if not line.startswith("O"):
            # add window to outlines
            #continue adding until i+window

            # if inside a region, don't add window
            # if outside a region, add the latest window
            if i > end:
                for w in wlines:
                    outlines.append(w)
            
            end = i+window
            
        if end > i:
            outlines.append(line)
        else:
            wlines.append(line)
            if len(wlines) > window:
                del wlines[0]
            
            
    return outlines


def densify(fname, outfname, window=-1, removetagless=False):
    """ Given a file, this will densify the file. That is,
    remove sentences with no tags, and keep only tokens
    within a window of labels. By default, this does nothing."""

    with codecs.open(fname, "r", "utf8") as f:
        lines = f.readlines()
        
    outlines = []
    sentlines = []
    hastag = False
    
    for line in lines:            
        sline = line.split("\t")
        if len(sline) > 5:
            tag = sline[0]
            if tag != "O":
                hastag = True
                
            sentlines.append(line)        
        else:
            if hastag or not removetagless:
                if window > 0:
                    sentlines = striptowindow(sentlines, window)
                    
                for sent in sentlines:
                    outlines.append(sent)
                sentlines  = []
                hastag = False
                outlines.append("\n")
            else:
                sentlines = []

    # in case the last lines are never added in.
    if len(sentlines) > 0 and (hastag or not removetagless):
        if window > 0:
            sentlines = striptowindow(sentlines, window)
                    
        for sent in sentlines:
            outlines.append(sent)
        
                
    with codecs.open(outfname, "w", "utf8") as out:
        for line in outlines:
            out.write(line);

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="This will densify a conll file. With no options, it does nothing.")

    parser.add_argument("file",help="Input file name")
    parser.add_argument("outfile",help="Output file name")
    parser.add_argument("--window", "-w",help="Window", type=int, default=-1)
    parser.add_argument("--removetagless", "-r",help="Remove tagless sentences", action="store_true")

    args = parser.parse_args()
    
    densify(args.file, args.outfile, args.window, args.removetagless)
