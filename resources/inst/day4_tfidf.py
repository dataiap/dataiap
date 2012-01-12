import os, sys, math, time
sys.path.append( os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../util')))
from email_util import *
from collections import Counter, defaultdict

import nltk
stemmer = nltk.stem.porter.PorterStemmer()

import re
refs_pat = '^[a-z][a-z\'-]+[a-z]$'
refs_prog = re.compile(refs_pat)
NAMEWORDS = set()

def l2norm(vec):
    return float(math.sqrt(sum(map(lambda (term, c): c**2, vec))))

def get_terms(s):
    return s.split()
    s = s.lower()
    lines = filter(lambda line: not line.strip().startswith(">"), s.split('\n'))
    arr = '\n'.join(lines).split()
    terms = []
    for term in arr:
        if re.match(refs_pat, term) != None:
            terms.append(term)
    terms = map(lambda term: term.replace("'s",'').replace("'", ''), terms)
    terms = filter(lambda term: len(term) > 3, terms)
    terms = filter(lambda term: term not in STOPWORDS, terms)
    terms = filter(lambda term: term not in NAMEWORDS, terms)
    terms = filter(stemmer.stem, terms)
            #return filter(lambda ngram: ' ' in ngram, [' '.join(terms[i:i+2]) for i in xrange(len(terms))])
    #terms.extend([' '.join(terms[i:i+2]) for i in xrange(len(terms))])
    return terms

for e in EmailWalker(sys.argv[1]):
    NAMEWORDS.update(e['names'])

start = time.time()
key_to_tf = defaultdict(Counter)
keycounts = Counter()
terms_by_key = defaultdict(set)
allterms = Counter()
nemails = 0
for e in EmailWalker(sys.argv[1]):
    try:
        words_in_email = set(get_terms(e['text']))
    except Exception as e:
        words_in_email = []
    if not len(words_in_email):
        #print "no words", e['folder']
        continue
    print e['folder'], e['sender']
    key = e['folder']
    key_to_tf[key].update(words_in_email)
    keycounts.update([key])
    #key_to_tf[e['folder']].update(words_in_email)
    unique_words_in_email = set(words_in_email)
    terms_by_key[key].update(unique_words_in_email)
    #allterms.update(unique_words_in_email)

print "parsing took", (time.time()-start)
nemails = len(terms_by_key)
for key, the_terms in terms_by_key.iteritems():
    allterms.update(the_terms)

# normalize tfs
for key in key_to_tf.keys():
    tfs = key_to_tf[key]
    normfactor = float(l2norm(tfs.iteritems()))
    #normfactor = float(keycounts[key] or 1)
    for term in tfs.keys():
        tfs[term] /= normfactor

start = time.time()
idfs = {}
for term, count in allterms.iteritems():
    idfs[term] = math.log( nemails / (1.0 + allterms[term]) )
print "idfs took", (time.time()-start)

# while True:
#     term = raw_input("input a : ")
#     if term == 'q': break
    
#     print key_to_tf['lay-k@enron.com'].get(term, -1),  idfs.get(term, -1)



start = time.time()
tfidfs = {}
for key, counter in key_to_tf.items():
    scores = filter(lambda pair: pair[1] > 0, [(term, count * idfs[term]) for term, count in counter.iteritems()] )
    scores.sort(key=lambda pair: pair[1], reverse=True)
    tfidfs[key] = dict(scores[:100])
print "tfidfs took", (time.time()-start)


print len(tfidfs)
l2norms = {}

allkeys = tfidfs.keys()

start = time.time()
for key, weights in tfidfs.iteritems():
    l2norms[key] = l2norm(weights.iteritems())
print "l2norm took", (time.time() - start)

start = time.time()

while True:
    key1 = raw_input("input key: ")
    if key1 not in allkeys:
        print "could not find key"
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

