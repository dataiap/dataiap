import math
import sys
from mrjob.protocol import JSONValueProtocol
from mrjob.job import MRJob
from term_tools import get_terms

class MRTermIDF(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, key, email):
        terms = set(get_terms(email['text']))
        for term in terms:
            yield term, 1

    def reducer(self, term, howmany):
        idf = math.log(516893.0 / sum(howmany))
        yield None, {'term': term, 'idf': idf}

if __name__ == '__main__':
        MRTermIDF.run()
