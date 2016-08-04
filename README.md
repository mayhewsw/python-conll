# python-conll

A collection of python scripts for working with CoNLL NER files.

compareanno.py
--------------

diff.py
-------

getstats.py
-----------
This will give statistics on a (labeled) corpus, such as number of tokens, and number of entities of each type.

mergelabels.py
--------------
Given a folder that is a labeled version of an original folder, this merges the updated labels back to the original.

preparelm.py
------------
This gathers words or sentences from a collection of CoNLL files in preparation for an LM or word vector training.

translate.py
------------
Given a word mapping file, this translates a set of CoNLL files.

util.py
-------
Some utilities.