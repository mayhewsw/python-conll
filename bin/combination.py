#!/home/mayhew2/miniconda3/bin/python
import os
from collections import defaultdict
from collections import Counter

def clean(lines):        
    while "DOCSTART" in lines[0] or len(lines[0].strip()) == 0:
        lines = lines[1:]
            
    while len(lines[-1].strip()) == 0:
        lines = lines[:-1]
            
    return lines

def func(folders, outfolder, comb):
    """ Args needs to be a list of foldernames. last is outfolder """

    fnamelists = []
    for arg in folders:
        # if this fails, abort!
        fnames = os.listdir(arg)
        fnamelists.append(fnames)
        
    # check to see that the same filenames exist here.
    #nameset = reduce(lambda a,b: set(a).add(set(b)), fnamelists)
    #if nameset != set(fnamelists[0]):
    #    # we have a problem!
    #    print("filename sets aren't the same...")
    #    exit()
        
        
    for fname in fnamelists[0]:
        print(fname)
        # open them both, compare lines.

        linelist = []
        for folder in folders:
            with open(folder + "/" + fname) as f:
                lines = clean(f.readlines())
                linelist.append(lines)

        # should probably ensure that the lengths are the same... oh well.

        writelines = []
        for t in zip(*linelist):

            ts = list(map(lambda l: l.split("\t"), t))

            # only check the first line.
            if len(ts[0]) > 5:
                
                word = ts[0][5]
                labels = list(map(lambda l: l[0], ts))

                #print(labels)
                
                # choose some strategy to pick a label.
                if comb == 1:
                    label = comb1(labels)
                elif comb == 2:
                    label = comb2(labels)
                elif comb == 3:
                    label = comb3(labels)
                else:
                    print("not a valid combination strategy!")
                    exit()
                
                ts[0][0] = label
                
                writelines.append("\t".join(ts[0]))

            else:
                writelines.append("\t".join(ts[0]))
                #print("\n")

        with open(outfolder + "/" + fname, "w") as out:
            for line in writelines:
                out.write(line)

def comb1(labels):
    # only if they all agree.
    if len(set(labels)) == 1:
        label = list(labels)[0]
    else:
        label = "O"

    return label

def comb2(labels):
    # majority vote

    c = Counter(labels)
    mc = c.most_common()
    label = mc[0][0]

    # a conflict, just return O
    if len(mc) > 1 and mc[0][1] == mc[1][1]:
            label = "O"
        
    return label


def comb3(labels):
    # if non-O label appears, use it.
    # majority vote, but O only wins if unanimous.

    labels = list(filter(lambda p: p != "O", labels))
    if len(labels) == 0:
        return "O"
    
    c = Counter(labels)
    mc = c.most_common()
    label = mc[0][0]

    # conflicts are resolved according to ordering.
    
    return label



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Merge two datasets together. Datasets must be identical in all but labels. Folder 2 will be merged into Folder 1. By default O labels will not be transferred. Use --overwrite option to overwrite O labels.")

    parser.add_argument("folders",help="merge into here", nargs="+")
    parser.add_argument("outfolder", help="out folder")
    parser.add_argument("comb", help="combination strategy", type=int, choices=[1,2,3])

    args = parser.parse_args()

    if len(args.folders) != 3:
        print("Probably want 3 folders!")
        exit()
    
    func(args.folders, args.outfolder, args.comb)

        

