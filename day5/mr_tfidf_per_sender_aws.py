#!/usr/bin/env python

from cStringIO import StringIO

from mrjob.protocol import JSONValueProtocol
from mrjob.job import MRJob
from mrjob.emr import EMRJobRunner

from term_tools import get_terms

class MRTFIDFBySender(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol

    def configure_options(self):
        super(MRTFIDFBySender, self).configure_options()
        self.add_passthrough_option(
            '--idf_loc', type='str', default='',
            help='The s3:// URL for the location of the IDFs')
        self.add_passthrough_option(
            '--aws_access_key_id', type='str', default='',
            help='The access key ID for the AWS account')
        self.add_passthrough_option(
            '--aws_secret_access_key', type='str', default='',
            help='The secret access key for the AWS account')

    def mapper(self, key, email):
        for term in get_terms(email['text']):
            yield {'term': term, 'sender': email['sender']}, 1

    def reducer_init(self):
        self.idfs = {}

        # Iterate through the files in the bucket provided by the user
        if self.options.aws_access_key_id and self.options.aws_secret_access_key:
            emr = EMRJobRunner(aws_access_key_id=self.options.aws_access_key_id,
                               aws_secret_access_key=self.options.aws_secret_access_key)
        else:
            emr = EMRJobRunner()

        for key in emr.get_s3_keys("s3://" + self.options.idf_loc):
            # Load the whole file first, then read it line-by-line: otherwise,
            # chunks may not be even lines
            for line in StringIO(key.get_contents_as_string()): 
                term_idf = JSONValueProtocol.read(line)[1] # parse the line as a JSON object
                self.idfs[term_idf['term']] = term_idf['idf']

    def reducer(self, term_sender, howmany):
        tfidf = sum(howmany) * self.idfs[term_sender['term']]
        yield None, {'sender': term_sender['sender'], 'term': term_sender['term'], 'tfidf': tfidf}

if __name__ == '__main__':
        MRTFIDFBySender.run()
