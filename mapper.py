#!/usr/bin/env python
"""mapper.py"""

import sys, re
from nltk.corpus import stopwords
from nltk import ngrams
N = int(sys.argv[1])
def cleaner(line):
    strippedList = re.sub(r'[^a-zA-Z ]+', ' ', line.replace("'","")).lower().replace("advertisement","").replace("\t"," ").strip().replace("\n"," ")
    strippedList =  ' '.join([word for word in strippedList.split() if word not in stopwords.words('english')])
    return strippedList

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = cleaner(line).strip()

    # split the line into words

    bigrams = ngrams(line.split(), N)
    words = [" ".join(grams) for grams in bigrams]

    # increase counters
    for word in words:
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        # tab-delimited; the trivial word count is 1
        print '%s\t%s' % (word, 1)