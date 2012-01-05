from aws_private_settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

import base64
import boto
import os
import sys

prefix = sys.argv[1]
num_accounts = int(sys.argv[2])

iam = boto.connect_iam(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

print "username,password,access_key_id,secret_access_id"
for i in range(num_accounts):
    username = "dataiap_%s_%d" % (prefix, i)
    password = base64.b64encode(os.urandom(100))[:10]
    user = iam.create_user(username)
    iam.add_user_to_group("dataiap_students", username)
    keys = iam.create_access_key(username)
    iam.create_login_profile(username, password)
    print "%s,%s,%s,%s" % (username, password, keys.access_key_id, keys.secret_access_key)
