#!/usr/bin/python
from conll.util import getfnames
from sklearn.metrics import f1_score, precision_score, recall_score

def func(fof1, fof2, ignore=False):
    print("THIS ONLY RETURNS TOKEN LEVEL")
    fnames1 = sorted(getfnames(fof1))
    fnames2 = sorted(getfnames(fof2))

    labels = set()
    gold = []
    pred = []
    for f1, f2 in zip(fnames1, fnames2):
        print(f1, f2)
        
        try:
            with open(f1) as f:
                lines = f.readlines()

            with open(f2) as f:
                lines2 = f.readlines()
        except IOError as e:
            print(e)
            continue

        i = 0
        j = 0
        total = 0
        while i < len(lines) and j < len(lines2):
            sline = lines[i].split("\t")
            sline2 = lines2[j].split("\t")
            
            try:
                while "-DOCSTART-" in lines[i] or lines[i].strip() == "":
                    i += 1
                    sline = lines[i].split("\t")

                while "-DOCSTART-" in lines2[j] or lines2[j].strip() == "":
                    j += 1
                    sline2 = lines2[j].split("\t")
            except IndexError:
                break
            
            if len(sline) < 5:
                continue

            try:
                predweight = sline2[6]
            except Exception:
                predweight = 1.0
                
            total += 1
            if ignore and float(predweight) == 0.0:
                pass
            else:
                gold.append(sline[0])
                pred.append(sline2[0])
                if sline[0] != "O":
                    labels.add(sline[0])
            
            #if sline[5] != sline2[5]:
            #    print("mismatching words!")
            #    print(sline[5])
            #    print(sline2[5])
            #    exit()

            i += 1
            j += 1

    labels = list(labels)
    p = precision_score(gold, pred, labels=labels, average="weighted")
    r = recall_score(gold, pred, labels=list(labels), average="weighted")
    f1 = f1_score(gold, pred, labels=list(labels), average="weighted")
    print("Scoring: {} lines out of {}".format(len(pred), total))
    print("SCORES: {} {} {}".format(p,r,f1))
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Get token level P/R/F1 scores.")

    parser.add_argument("folder", help="gold input file or folder")
    parser.add_argument("outfolder", help="predicted output file or folder")
    parser.add_argument("--ignore", help="ignore all words with a 0 weight.", action="store_true")

    args = parser.parse_args()

    func(args.folder, args.outfolder, args.ignore)

