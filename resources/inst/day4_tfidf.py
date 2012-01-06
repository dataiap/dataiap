import os, sys, math, time
sys.path.append( os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../util')))
from email_util import *
from collections import Counter, defaultdict


import re
refs_pat = '^[a-z][a-z\'-]+[a-z]$'
refs_prog = re.compile(refs_pat)


def get_terms(s):
    s = s.lower()
    lines = filter(lambda line: line.strip().startswith(">"), s.split('\n'))
    arr = '\n'.join(lines).split()
    terms = []
    for term in arr:
        if re.match(refs_pat, term) != None:
            terms.append(term)
    terms = filter(lambda term: len(term) > 3, terms)
    terms = filter(lambda term: term not in STOPWORDS, terms)
    return terms

    
start = time.time()
key_to_tf = defaultdict(Counter)
allterms = Counter()
nemails = 0
for e in EmailWalker(sys.argv[1]):
    try:
        words_in_email = set(get_terms(e.text))
    except:
        words_in_email = []
    if not len(words_in_email):
        continue
    print e.folder, e.sender
    key_to_tf[e.sender].update(words_in_email)
    #key_to_tf[e.folder].update(words_in_email)
    unique_words_in_email = set(words_in_email)
    allterms.update(unique_words_in_email)
    nemails += 1
print "parsing took", (time.time()-start)

start = time.time()
idfs = {}
for term, count in allterms.iteritems():
    idfs[term] = math.log( nemails / (1 + allterms[term]) )
print "idfs took", (time.time()-start)

start = time.time()
tfidfs = {}
for key, counter in key_to_tf.items():
    tfidfs[key] = dict(filter(lambda pair: pair[1] > 0, [(term, count * idfs[term]) for term, count in counter.iteritems()] ))
print "tfidfs took", (time.time()-start)

def l2norm(vec):
    return float(math.sqrt(sum(map(lambda (term, c): c**2, vec))))

print len(tfidfs)
l2norms = {}

allkeys = tfidfs.keys()

start = time.time()
for key, weights in tfidfs.iteritems():
    l2norms[key] = l2norm(weights.iteritems())
print "l2norm took", (time.time() - start)

start = time.time()

while True:
    key1 = raw_input("input email: ")
    if key1 not in allkeys:
        print "could not find email"
        continue



    print "top tfidfs"
    for pair in sorted(tfidfs[key1].items(), key=lambda (k,v): v, reverse=True)[:10]:
        print '\t', pair    
    
    #for idx, key1 in enumerate(allkeys):
    similarities = {}
    if True:
        #for key2 in allkeys[idx+1:]:
        for key2 in allkeys:
            weights1 = tfidfs[key1]
            weights2 = tfidfs[key2]
            overlap = [(term, c*weights2[term]) for term, c in weights1.iteritems() if term in weights2]
            numerator = float(sum(map(lambda (k,v): v, overlap)))
            denominator = l2norms[key1] * l2norms[key2] + 1.0
            similarities[(key1, key2)] = (numerator / denominator, overlap)
    print "similarities took", (time.time() - start)


    for emails, data in sorted(similarities.items(), key=lambda (emails, data): data[0], reverse=True)[:5]:
        print data[0], '\t', emails
        overlap = data[1]
        overlap.sort(key=lambda (k,v): v, reverse=True)
        for term, score in overlap[:10]:
            print '\t', score, '\t', term

