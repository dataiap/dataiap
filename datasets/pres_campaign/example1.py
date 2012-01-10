#!/usr/bin/env python

import csv,sys,datetime
reader = csv.DictReader(open(sys.argv[1], 'r'))

for row in reader:
    name = row['cand_nm']
    datestr = row['contb_receipt_dt']
    amount = row['contb_receipt_amt']
    print ','.join([name, datestr, amount])

