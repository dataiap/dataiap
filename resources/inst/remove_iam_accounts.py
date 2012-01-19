from aws_private_settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

import base64
import boto
import csv
import os
import sys

reader = csv.DictReader(open(sys.argv[1], 'r'))
iam = boto.connect_iam(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

for line in reader:
    username = line['username']
    key_id = line['access_key_id']
    try:
        user = iam.delete_login_profile(username)
    except:
        pass
    iam.remove_user_from_group("dataiap_students", username)
    iam.delete_access_key(key_id, username)
    iam.delete_user(username)

