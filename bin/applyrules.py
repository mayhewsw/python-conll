#!/home/mayhew2/miniconda3/bin/python
import os.path
from conll.readconll import readconll
from conll.ConllDocument import Constituent
from collections import defaultdict


def func(folder, outfolder, ruleslist):
    fnames = os.listdir(folder)

    with open(ruleslist) as f:
        rules = list(map(lambda l: l.strip().split("\t"), f.readlines()))

    i = 0

    for fname in fnames:
        print(fname)
        i += 1
        cdoc = readconll(folder + "/" + fname)
        cdoc.clearconstituents()

        ind1 = defaultdict(list)
        ind2 = defaultdict(list)
        ind3 = defaultdict(list)
        ind4 = defaultdict(list)
        ind5 = defaultdict(list)

        for j, t in enumerate(cdoc.tokens):
            ind1[t.s].append("{}:{}:{}".format(fname, j, j+1))
            ind2[" ".join(c.s for c in cdoc.tokens[j:j+2])].append("{}:{}:{}".format(fname, j, j+2))
            ind3[" ".join(c.s for c in cdoc.tokens[j:j+3])].append("{}:{}:{}".format(fname, j, j+3))
            ind4[" ".join(c.s for c in cdoc.tokens[j:j+4])].append("{}:{}:{}".format(fname, j, j+4))
            ind5[" ".join(c.s for c in cdoc.tokens[j:j+5])].append("{}:{}:{}".format(fname, j, j+5))

        for i, r in enumerate(rules):
            #if i%5000 == 0:
            #    print("on rule {} out of {}".format(i, len(rules)))
            label = r[0]
            entity = r[1]

            matches = []
            for ind in [ind5, ind4, ind3, ind2, ind1]:
                if entity in ind:
                    matches = ind[entity]
                    break

            if len(matches) > 0:
                for match in matches:
                    f, s, e = match.split(":")
                    # FIXME: proceed only if fname matches the conlldocument
                    toks = cdoc.tokens[int(s):int(e)]
                    c = Constituent(label, toks, (int(s), int(e)))
                    cdoc.addconstituent(c)

        with open(outfolder + "/" + os.path.basename(fname), "w") as out:
            cdoc.write(out)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("folder", help="")
    parser.add_argument("outfolder", help="")
    parser.add_argument("ruleslist", help="Should have format: label<tab>entity")

    args = parser.parse_args()
    func(args.folder, args.outfolder, args.ruleslist)
