from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol, JSONValueProtocol, PickleProtocol

import sys

class MRtf(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    INTERNAL_PROTOCOL = JSONProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, key, line):
        if line['type'] != 'document':
            raise Error("I only process documents!")
        for word in line['document'].split():
            yield word, 1

    def reducer(self, word, occurrences):
        yield None, {"type": "idf", "word": word, "sum": sum(occurrences)}

if __name__ == '__main__':
        MRtf.run()

