import csv,sys,datetime,collections
import numpy
import scipy.stats
import welchttest

# for scipy stats reference, see: http://docs.scipy.org/doc/scipy/reference/stats.html
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
print len(obama), len(mccain)

# certainly the means look different...
print "Obama mean, stdev", numpy.mean(obama), numpy.std(obama)
print "McCain mean, stdev", numpy.mean(mccain), numpy.std(mccain)

# running a ttest of independent samples suggests that they aren't the same mean
print "ttest, equal variances", scipy.stats.ttest_ind(obama, mccain)

# small white lie: there is no reason to believe that these two samples have
# equal variance, so let's use a welch test.
print "welch", welchttest.welchs_approximate_ttest_arr(obama, mccain)

# but we've been lying to you.  you should only run ttests on normal data, so run
# the shapiro-wilk test of normalcy
print "obama shapiro", scipy.stats.shapiro(obama)
print "mccain shapiro", scipy.stats.shapiro(mccain)

# ooops...we have to reject the null hypothesis: it's very unlikely these two
# are normally distributed.  it's actually not that bad for a ttest, but just to
# be sure, let's run a non-parametric test called the Mann-Whitney U test.
print "mann-whitney U", scipy.stats.mannwhitneyu(obama, mccain)

# cool!  the p-value is 0.  So if our alpha was .05 or .01, we'd still be below
# it.  it's unlikely these two are from the same distribution, and thus we
# can safely reject the null hypothesis that they have the same mean.  Obama's
# donations were really smaller than McCain's!



# At this point, let's convince ourselves by plotting a histogram of their contributions
# in 100 dollar increments.
#

increment = 100
width=50
obama_bucketed = map(lambda amount: amount - amount%increment, obama)
mccain_bucketed = map(lambda amount: amount - amount%increment, mccain)
# in python 2.7+, we can use the Counter class
# in python 2.6, you can use defaultdict
from collections import Counter
obama_hist = Counter(obama_bucketed)
mccain_hist = Counter(mccain_bucketed)
minamount = min(min(obama), min(mccain))
maxamount = max(max(obama), min(mccain))
print "min/max", minamount, maxamount
buckets = range(int(minamount), int(maxamount+1), increment)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

fig = plt.figure()
subplot = fig.add_subplot(111)
subplot.bar(obama_hist.keys(), obama_hist.values(), color='b', edgecolor='b', label="Obama")#, s=1)
subplot.bar(mccain_hist.keys(), mccain_hist.values(), color='r', edgecolor='r', label="McCain")#, s=1)

# We can't see anything without a log scale
#subplot.set_yscale('log')
# there are anamolous donations in the 100k and millions that we don't want to see
subplot.set_xlim((-20000, 20000))

subplot.legend()
plt.savefig('../../day3/figures/mccain-obama-histogram.png', format='png')


fig = plt.figure()
subplot = fig.add_subplot(111)
subplot.boxplot([obama, mccain], whis=1)
subplot.set_ylim((-250, 1250))
subplot.set_xticklabels(("Obama", "McCain"))
subplot.set_title("Obama vs. McCain Contributions")
plt.savefig('../../day3/figures/mccain-obama-boxplot.png', format='png')
