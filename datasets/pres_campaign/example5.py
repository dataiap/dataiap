#!/usr/bin/env python

# Negative donations

from   collections import defaultdict
import matplotlib.pyplot as plt
import csv, sys
from   datetime import datetime

reader = csv.DictReader(open(sys.argv[1], 'r'))

for row in reader:
    name = row['cand_nm']
    datestr = row['contb_receipt_dt']
    amount = float(row['contb_receipt_amt'])

    if amount < 0:
        print '\t'.join(row.values())
