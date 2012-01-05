"""
Uploads Ap data to S3

"""



import os, sys
from news_util import walk_news
from boto.s3.connection import S3Connection
from boto.s3.key import Key
accesskey = ''
secretkey = ''
conn = S3Connection(accesskey, secretkey)

bucketname = 'dataiap.mit.edu.ap'
try:
    bucket = conn.create_bucket(bucketname)
except:
    print "could not create bucket ", bucketname
    bucket = conn.get_bucket(bucketname)



def upload(category, fname, root):
    if fname.startswith('urn'):
        key = Key(bucket)
        key.key = '%s_%s' % (category, fname)
        key.set_contents_from_filename('%s/%s' % (root, fname))

root = os.path.abspath(sys.argv[1])
walk_news(root, upload)

# retrieve ALL articles in World
bucket.get_all_keys(prefix='World')
conn.close()


# return self._get_all([('CommonPrefixes', Prefix)],
#                       '', None, {})
