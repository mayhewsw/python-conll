from setuptools import setup

setup(name='conll',
      version='0.1',
      description='The funniest joke in the world',
      url='http://github.com/mayhew2/python-conll',
      author='Scripts for NER CoNLL format files',
      author_email='swm.mayhew@gmail.com',
      license='MIT',
      packages=['conll'],
      scripts=['bin/applyrules.py',
               'bin/combination.py',
               'bin/compare.py',
               'bin/conll2submission.py',
               'bin/count.py',
               'bin/densify.py',
               'bin/encodestems.py',
               'bin/gazmatch.py',
               'bin/getnames.py',
               'bin/getstats.py',
               'bin/perturb.py',
               'bin/iaa.py',
               'bin/mergelabels.py',
               'bin/stemfile.py',
               'bin/stem.py',
               'bin/toconll.py',
               'bin/tolines.py',
               'bin/translate.py',
               'bin/modifylabels.py',
               'bin/twitterner.py'
      ]
      ,
      zip_safe=False)

