#!/usr/bin/env python

from   collections import defaultdict
import matplotlib.pyplot as plt
import csv, sys
from   datetime import datetime

reader = csv.DictReader(open(sys.argv[1], 'r'))

obamadonations = defaultdict(lambda:0)

for row in reader:
    name = row['cand_nm']
    datestr = row['contb_receipt_dt']
    amount = float(row['contb_receipt_amt'])
    date = datetime.strptime(datestr, '%d-%b-%y')

    if 'Obama' in name:
        obamadonations[date] += amount

# dictionaries 
sorted_by_date = sorted(obamadonations.items(), key=lambda (key,val): key)
xs,ys = zip(*sorted_by_date)
plt.plot(xs, ys, label='line 1')
plt.legend(loc='upper center', ncol = 4)
plt.savefig('obamadonations.png', format='png')

