import re
import sys
from collections import defaultdict
from mrjob.protocol import JSONValueProtocol
from term_tools import get_terms

input = open(sys.argv[1])
words = defaultdict(lambda: 0)
for line in input:
    email = JSONValueProtocol.read(line)[1]
    for term in get_terms(email['text']):
        words[term] += 1

for word, count in words.items():
    print word, count
