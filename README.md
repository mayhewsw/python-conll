# python-conll

A collection of python scripts for working with CoNLL NER files.

# Installation

```
$ https://github.com/CogComp/python-conll.git
$ cd python-conll
$ python setup.py install
```

# CoNLL NER Format
This library assumes a column format, where columns are separated by tabs, and columns
tend to have specific meanings.

Column 0 is the tag.
Column 5 is the word.

All other columns can mean whatever you want them to. For example, column 6 often holds the weight. See an example file [here](conll/tests/sample.txt.conll). 
