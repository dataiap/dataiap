import csv, random, sys, datetime, os
from common import *
random.seed(0)



reader = csv.DictReader(open(sys.argv[1], 'r'))
if len(sys.argv) > 2:
    prob = float(sys.argv[2])
else:
    prob = 0.3
idx = 0


for row in reader:
    if random.random() > prob:
        continue
    name = row['cand_nm']
    datestr = row['contb_receipt_dt']
    amount = float(row['contb_receipt_amt'])
    date = datetime.datetime.strptime(datestr, '%d-%b-%y')
    zipcode = row['contbr_zip']
    state = row['contbr_st']
    city = row['contbr_city']
    job = row['contbr_occupation']
    memo = row['memo_text']
    reason = row['receipt_desc']

    
    name = name.replace(',', '')
    job = job.replace(',','')
    memo = memo.replace(',','')
    reason = reason.replace(',', '')
    # if state not in abbrtoname:
    #     print >>sys.stderr, "state not found:", state
    #     print >>sys.stderr, city, state, zipcode
    #     break
    #     continue

    print ','.join(map(str, [name,
                             date.strftime('%Y-%m-%d'),
                             amount,
                             abbrtoname[state],
                             zipcode,
                             job,
                             reason,
                             memo]))
    idx += 1
    if idx % 100000 == 0:
        print "processed", idx
    
