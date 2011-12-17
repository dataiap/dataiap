import csv,sys,datetime,collections
import itertools
import matplotlib.pyplot as plt
import rpy2.robjects as R
import numpy
import rpy_helper


# requires R
# requires rpy2
# to install matplot lib, see https://jholewinski.wordpress.com/2011/07/21/installing-matplotlib-on-os-x-10-7-with-homebrew/
reader = csv.DictReader(open(sys.argv[1], 'r'))
idx = 0

candtomoney = collections.defaultdict(list)

for row in reader:
    name = row['cand_nm']
    amount = float(row['contb_receipt_amt'])
    candtomoney[name].append(amount)

obama = candtomoney["Obama Barack"]
mccain = candtomoney["McCain John S"]

print "Obama mean, stdev", numpy.mean(obama), numpy.std(obama)
print "McCain mean, stdev", numpy.mean(mccain), numpy.std(mccain)

args = {'var.equal': False, 'paired': False}
result = rpy_helper.pify(R.r["t.test"](R.FloatVector(obama), R.IntVector(mccain), **args))
print result['p.value'], result['statistic'], result['method'], result.keys()
