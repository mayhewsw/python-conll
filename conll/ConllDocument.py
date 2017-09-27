#!/home/mayhew2/miniconda3/bin/python

class ConllDocument:
    """
    This doc is super cool. The main point of this class
    is to store names, along with their token/character offsets,
    having read that from conll. 
    """

    def __init__(self,tokens, spans, labels, sentenceends):
        self.tokens = tokens
        self.spans = spans
        self.labels = labels
        self.sentenceends = sentenceends

        self._constituents = []
        
        for label,span in zip(labels,spans):
            c = Constituent(label, self.tokens[span[0]:span[1]], span)
            self._constituents.append(c)

    def __init__(self,tokens, constituents, sentenceends):
        self._constituents = constituents

        self.labelmap = {}

        self.sentenceends = sentenceends
        
        for c in self._constituents:
            
            for i in range(c.span[0], c.span[1]):
                if i == c.span[0]:
                    self.labelmap[i] = "B-" + c.label
                else:
                    self.labelmap[i] = "I-" + c.label
            
        self.tokens = tokens

    def getconstituents(self):
        return list(self._constituents)

    def removeconstituent(self, c):
        if c in self._constituents:
            self._constituents.remove(c)

            for i in range(c.span[0], c.span[1]):
                if i in self.labelmap:
                    del self.labelmap[i]
                        
            return True
        
        else:
            return False
            
    def findmatches(self, s):
        ss = s.split(" ")
        ret = []
        
        for i,t in enumerate(self.tokens):
            if i+len(ss) > len(self.tokens):
                break
            span = (i,i+len(ss))
            curr = self.getString(span)
            if s == curr:
                ret.append(span)
            else:
                pass
        return ret

    def write(self, out):
        for i, token in enumerate(self.tokens):
            if i in self.sentenceends:
                out.write("\n")
            
            if i in self.labelmap:
                label = self.labelmap[i]
            else:
                label = "O"

            outlst = [label, "0", str(i), "x", "x", token.s, "x", "x", "0"]
            
            out.write("\t".join(outlst) + "\n")
        out.write("\n")
                

            
    def addConstituent(self, c):
        # TODO: check for overlap! and don't allow if so.
        self._constituents.add(c)        
    
    def getString(self,span):
        return " ".join(map(str,self.tokens[span[0]:span[1]]))

    def getCharSpan(self,span):
        start = self.tokens[span[0]].start
        end = self.tokens[span[1]-1].end
        return start,end
    
    def __repr__(self):
        return " ".join(map(str,self.tokens))

class Constituent:
    """ This consists of a
    label, a tokenized surface form and
    offsets """

    def __init__(self, label, tokens, span):
        self.label = label
        self.tokens = tokens
        self.span = span

    def surf(self):
        return " ".join(map(str, self.tokens))

    def __repr__(self):
        return "[" + self.label + " " + " ".join(map(str, self.tokens)) + "]"

    def __eq__(self, other):
        return self.label == other.label and self.span == other.span
    

class Token:
    def __init__(self, start, end, s):
        self.start = start
        self.end = end
        self.s = s

    def __repr__(self):
        return self.s

    def __str__(self):
        return self.s
