#! /home/mayhew2/miniconda3/bin/python
import os
from collections import defaultdict
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import confusion_matrix

def sortmap(m, k=20):
    """ Sort a dictionary by value, return the top k """
    return sorted(m.items(), key=lambda p: p[1], reverse=True)[:k]


def func(folder1, folder2):

    labs1 = []
    labs2 = []
    
    oldfnames = os.listdir(folder1)
    newfnames = os.listdir(folder2)

    counts = defaultdict(int)
    wordcounts = defaultdict(int)

    for fname in oldfnames:
        if fname not in newfnames:
            print("UH OH")
        else:
            print(fname)
            # open them both, compare lines.            
            with open(folder1 + "/" + fname) as f:
                lines1 = f.readlines()
            with open(folder2 + "/" + fname) as f:
                lines2 = f.readlines()

            if len(lines1) != len(lines2):
                print("!!! length of files doesn't match. Old:",len(lines1)," New:",len(lines2))
                return
                
            for old,new in zip(lines1, lines2):
                sold = old.split("\t")
                snew = new.split("\t")
                if len(sold) > 5 and len(snew) > 5: 
                    labs1.append(sold[0])
                    labs2.append(snew[0])
                    counts[sold[0] + ":" + snew[0]] += 1
                    if sold[0] != snew[0]:
                        wordcounts[sold[0] + ":" + snew[0] + ":" + sold[5]] += 1
                    
    k = cohen_kappa_score(labs1, labs2)
    print("cohen's kappa", k)

    labels = sorted(set([key.split(":")[0] for key in counts]))
    #from sklearn.metrics import confusion_matrix

    print(labels)
    print(confusion_matrix(labs1, labs2, labels = labels))

    miss =0
    disagreement = 0
    agree = 0
    
    for key in counts:
        # ignore all matching.
        if key == "O:O":
            continue
        
        if len(set(key.split(":"))) == 1:
            agree += counts[key]
        elif "O" in key.split(":"):
            miss += counts[key]
        else:
            disagreement += counts[key]
            
    print("agree:", agree)
    print("miss:", miss)
    print("disagreement:", disagreement)

    for misses in sortmap(wordcounts, k=20):
        print(misses)
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("folder1",help="")
    parser.add_argument("folder2",help="")

    args = parser.parse_args()
    
    func(args.folder1, args.folder2)
