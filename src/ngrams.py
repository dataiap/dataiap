from collections import Counter, defaultdict
import os, sys, math, nltk


stopwords = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'])
stemmer = nltk.stem.porter.PorterStemmer()

def get_ngrams(s, n = 1):
    s = s.lower()
    arr = s.split()
#    arr = map(stemmer.stem, arr)
    ngrams = [tuple(arr[idx:idx+n]) for idx in xrange(0, len(arr) - n)]
    ngrams = filter(lambda ngram: len(stopwords.intersection(ngram))<n, ngrams)
    return map(lambda ngram: ' '.join(ngram), ngrams)


root = os.path.abspath(sys.argv[1])
artcount = defaultdict(Counter)
cat2art = defaultdict(list)
catcount = defaultdict(Counter)
corpuscount = Counter()
narticles = 0
for root, dirs, files in os.walk(root):
    category = os.path.basename(root)
    print category
    for fname in files:
        if fname.startswith('urn'):
            with open('%s/%s' % (root, fname), 'r') as f:
                article_text = f.read()
                for n in [1, 2]:
                    ngrams = get_ngrams(article_text, n)
                    artcount[fname].update(ngrams)
                    catcount[category].update(ngrams)
                    corpuscount.update(ngrams)
            cat2art[category].append(fname)
            narticles += 1




            
#
# Cross Category TFIDF
#        
# idf:
#
idfs = defaultdict(lambda:0)
for term, count in corpuscount.iteritems():
    idfs[term] = math.log(float(narticles) / count)

# tfidf
for cat, counter in catcount.iteritems():
    tf = defaultdict(lambda:0)
    for term, count in counter.iteritems():
        tf[term] = count * idfs[term]
    catterms = list(tf.items())
    catterms.sort(lambda a,b: a[1] < b[1] and 1 or -1)
    print cat
    for x in catterms[:10]:
        print '\t', x


#
# per article tfidf:
#
# use the terms with tfidf > 0 in the global tfidf

# catcount = defaultdict(Counter)
# corpuscount = Counter()
art2tfidf = {}        
for category in cat2art.keys():
    ncatarticles = float(len(cat2art[category]))
    for artname in cat2art[category]:
        counter = artcount[artname]
        tfidf = {}
        for term, n in counter.iteritems():
            idf = math.log(ncatarticles / (catcount[category][term]+1))
            tfidf[term] = n * idf
        tfidf = dict(filter(lambda (t,n): n > 0, tfidf.items()))




