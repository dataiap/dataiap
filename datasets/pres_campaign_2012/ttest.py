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
