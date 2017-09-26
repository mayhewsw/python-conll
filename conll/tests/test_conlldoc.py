#!/home/mayhew2/miniconda3/bin/python
from unittest import TestCase

import conll,sys
import os.path
from conll.readconll import *

class TestDoc(TestCase):

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    def test_read(self):
        
        doc = readconll(os.path.join(self.__location__,"sample.txt.conll"))
        self.assertTrue(len(doc.getconstituents()) == 11)
        
    def test_remove(self):
        doc = readconll(os.path.join(self.__location__,"sample.txt.conll"))

        cons = list(doc.getconstituents())
        
        for c in cons:
            doc.removeconstituent(c)            

        self.assertEqual(len(doc.getconstituents()), 0)
                
