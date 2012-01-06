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
  get s3prefix destination_directory
  put source_directory s3bucket
  rm  s3prefix
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

def parse_prefix(prefix):
    if protocol in prefix:
        prefix = prefix[len(protocol):]
    if '/' in prefix:
        idx = prefix.find('/')
        bucketname = prefix[:idx]
        searchterm = prefix[idx+1:]
    else:
        bucketname = prefix
        searchterm = None
    return (bucketname, searchterm)

if cmd == 'get':
    prefix = sys.argv[2]
    outdir = sys.argv[3]


    if not os.path.exists(outdir) or not os.path.isdir(outdir):
        raise Error("%s is not a directory or does not exist!" % outdir)

    (bucketname, searchterm) = parse_prefix(prefix)
    b = conn.get_bucket(bucketname)
    kiter = b.list(searchterm)
    for key in kiter:
        dirs = key.key.split("/")[:-1]
        for diridx in xrange(len(dirs)):
            tmpdir = os.path.join(outdir, *dirs[:diridx+1])
            try:
                os.mkdir(tmpdir)
            except:
                pass

        f = file(os.path.join(outdir, key.key), 'w')
        f.write(key.read())
        f.close()
elif cmd == 'put':
    sourcedir = sys.argv[2]
    prefix = sys.argv[3]

    if not os.path.exists(sourcedir) or not os.path.isdir(sourcedir):
        raise Error("%s is not a directory or does not exist!" % sourcedir)
        
    (bucketname, searchterm) = parse_prefix(prefix)

    if searchterm != None:
        raise Error("You should only specify a bucket here")
    
    bucket = conn.create_bucket(bucketname)
    for file in os.listdir(sourcedir):
        key = Key(bucket)
        key.key = file
        key.set_contents_from_filename(os.path.join(sourcedir, file))

elif cmd == 'rm':
    print "not implemented"
    exit()

try:
    conn.close()
except:
    pass
