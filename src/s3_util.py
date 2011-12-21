"""
Download a set of files from S3 into a local folder

Usage: python s3_download.py COMMAND OUTPUTDIR [s3prefix, ...]

Example: python s3_download.py get ./s3files s3://dataiap.mit.edu.news/
         downloads all files in s3://dataiap.mit.edu.news/ into ./s3files
"""

import os, sys
from boto.s3.connection import S3Connection
from boto.s3.key import Key



if len(sys.argv) < 2 or sys.argv[1] in ('help', 'h'):
    s = """
Commands:
  get OUTDIR [s3prefix, ...]
  rm  [s3prefix, ...]
    """
    print s
    exit()
try:
    awskey = os.environ['AWS_ACCESS_KEY_ID']
    awssecret = os.environ['AWS_SECRET_ACCESS_KEY']
except:
    print "set the environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY"
    exit()

protocol = 's3://'
conn = S3Connection(awskey, awssecret)
cmd = sys.argv[1]


if cmd == 'get':
    outdir = sys.argv[2]
    prefixes = sys.argv[3:]

    if not os.path.exists(outdir) or not os.path.isdir(outdir):
        print "%s is not a directory or does not exist!" % outdir
        exit()
    
    for prefix in prefixes:

        if protocol in prefix:
            prefix = prefix[len(protocol):]
        if '/' in prefix:
            idx = prefix.find('/')
            bucketname = prefix[:idx]
            searchterm = prefix[idx+1:]
        else:
            bucketname = prefix
            searchterm = None

        b = conn.get_bucket(bucketname)
        kiter = b.list(searchterm)
        for key in kiter:
            # create the directory structure
            dirs = os.path.split(key.key)[:-1]
            for diridx in xrange(len(dirs)):
                tmpdir = os.path.join(outdir, *dirs[:diridx+1])
                try:
                    os.mkdir(tmpdir)
                except:
                    pass

            f = file(os.path.join(outdir, key.key), 'w')
            f.write(key.read())
            f.close()
elif cmd == 'rm':
    print "not implemented"
    exit()

try:
    conn.close()
except:
    pass
