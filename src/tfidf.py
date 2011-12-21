from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol, JSONValueProtocol, PickleProtocol
import collections

class MRtfidf(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    INTERNAL_PROTOCOL = JSONProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol
    
    def mapper(self, key, line):
        if line['type'] == 'idf':
            yield line['word'], line
        elif line['type'] == 'document':
            for word in line['document'].split():
                yield word, {"type": "tf", "docid": line['docid']}
    def reducer(self, word, items):
        materialized = list(items)
        idf = filter(lambda x: x['type'] == 'idf', materialized)[0]['sum']
        doc_words = filter(lambda x: x['type'] == 'tf', materialized)
        counts = collections.defaultdict(lambda: 0)
        for dw in doc_words:
            counts[dw['docid']] += 1.0/idf
        for k, v in counts.iteritems():
            yield None, {'type': 'tfidf', 'docid': k, 'word': word, 'tfidf': v}

if __name__ == '__main__':
        MRtfidf.run()
