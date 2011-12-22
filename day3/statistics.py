#!/usr/bin/env python

# So far, we've plotted and visualized data in various ways.  Today,
# we'll see how to statistically back up some of the observations
# we've made in looking at our data.  Statistics is a tool that helps
# separate newsmaking data-backed stories from one-off anecdotes.
# Usually, both kinds of stories start with a hunch, and statistics
# helps us quantify the evidence backing that hunch.
# 
# Whenever you have a hunch (a **hypothesis** in statistician-speak),
# the first thing to do is to look at some summary statistics (e.g.,
# averages), and explore the data graphically as we did yesterday.  If
# the visualizations seem to support your hunch, you will move into
# hypothesis-testing mode.
# 
# Today, we'll show differences between the Obama and McCain campaigns
# in 2008 using statistical tests. We'll also use the
# [County Health Ranking]($$$) to identify ways to predict mortality
# rates across communities in the United States.
#
# <h3>Comparing means using T-Tests</h3>
#
# For our first set of tests, we're going to use two running examples:
# campaign spending and a fun comparison of two towns' citizens' heights.  Here are the two scenarios:
#
#
#   * One thing that's been claimed about the 2008 election is that
# President Obama raised smaller quantities from a larger group of
# donors than Senator McCain, who raised a smaller number of large
# contributions.  Statistical techniques will help us determine how
# true this statement is.
#   * Imagine two towns that only differ in
# that one of the twons had "something in the water" the year a bunch
# of kids were born.  Did that something in the water affect the
# height of these kids?  (Note: this situation is not realistic.  it's
# never the case that the only difference between two communities is
# the one you want to measure, but it's a nice goal!)  We'll use statistics
# to determine whether the two communities have meaninfully different heights.
#
# <h4>Comparing Averages</h4>
#
# 
# show averages for both height and campaign.  they are different.  how different?
# visual approach: histogram.  impossible.  so show boxplot.  then show code for height boxplot.  then have them make campaign boxplot.
# then there's a problem: how much overlap is good or bad?  need math for this!
# t test
#
# Let's start by comparing a simple statistic, to see if in the data
# we observe there's any difference.  We'll start by comparing the
# average heights of the two towns

import numpy
town1_heights = [5, 6, 7, 6, 7.1, 6, 4]
town2_heights = [5.5, 6.5, 7, 6, 7.1, 6]

town1_mean = numpy.mean(town1_heights)
town2_mean = numpy.mean(town2_heights)

print "Town 1 avg. height", town1_mean
print "Town 2 avg. height", town2_mean

print "Effect size: ", abs(town1_mean - town2_mean)

# It looks like town 2's average height ($$$ feet) is higher than
# town 1 ($$$ feet) by a difference of $$$ feet.  This difference is
# called the ** Effect size **.  Town 2 certainly looks taller than
# Town 1!
#
# ** Exercise ** Compute the average campaign contribution for the
# Obama and McCain campaigns from the dataset in day 1.  What's the
# effect size?  We have an average contribution of $$$ for McCain and
# $$$ for Obama, for an effect size of $$$.  McCain appears, on
# average, to have more giving donors.
#
# Before we fire up the presses on either of these stories, let's look
# at the data in more depth.
#
# <h5>Graph The Data</h5>
#
# The effect size in both of our examples seems large.  It would be
# nice to more than just compare averages.  Let's try to look at a
# histogram of the distributions.  We created a histogram of the two
# campaigns contributions, binned by $100 increments.

import matplotlib.pyplot as plt
from collections import Counter


increment = 1
width= .25

town1_bucketted = map(lambda ammt: ammt - ammt%increment, town1_heights)
town2_bucketted = map(lambda ammt: ammt - ammt%increment + width, town2_heights)
town1_hist = Counter(town1_bucketted)
town2_hist = Counter(town2_bucketted)

minamount = min(min(town1_heights), min(town2_heights))
maxamount = max(max(town1_heights), max(town2_heights))
buckets = range(int(minamount), int(maxamount)+1, increment)

fig = plt.figure()
plt.bar(town1_hist.keys(), town1_hist.values(), color='b', width=width, label="town 1")
plt.bar(town2_hist.keys(), town2_hist.values(), color='r', width=width, label="town 2")
plt.legend()
plt.show()

#
# This results in a histogram that looks like this:
#
# $$$
#
# Not bad!  The buckets are all exactly the same size except for $$$ in town $$$.
#
# ** Exercise ** Build a histogram for the Obama and McCain campaigns.  This is challenging, because there are a large number of outliers that make the histograms difficult to compare.  Add the line

plt.set_xlim((-20000, 20000))

# before displaying the plot in order to set the x-values of the histogram to cut off donations larger than $20,000 or smaller than $20,000.  With bar widths of $$$ and increments of $100, your histogram will look something like this:
#
# $$$
# 
# Ouch!  I can't make heads or tails of that.  For large datasets, a
# histogram might have too much information on it to be helpful.
# Luckily, descriptive statisticians have a more concise
# visualization.  It's called a box-and-whisker plot!  The code for it is quite simple as well:

import matplotlib.pyplot as plt

fig = plt.figure()
plt.boxplot([town1_heights, town2_heights], whis=1)
plt.show()

# Here's what we see:
# 
# $$$ img
#
# 
# Let's interpret this plot.  We show town 1 on the left and town 2 on
# the right.  Each town is represented by a box with a red line and
# whiskers.

# * The red line in the box represents the ** median **, or
# ** 50th percentile ** value of the distribution.  If we sort the
# dataset, 50% of the values will be below this line, and 50% will be
# above it.
#   * The bottom edge of the box represents the ** 25th percentile **
# (the value larger than 25% of your dataset), and the top edge
# represents the ** 75th percentile ** (the value larger than 75% of
# your dataset).  The difference between the 75th and 25th percentile
# is called the ** inner quartile range (IQR) **.
#   * The whiskers represent the "extremes" of your dataset: the
#   largest value we're willing to consider in our dataset before
#   calling it an outlier.  In our case, we set ** whis=1 **,
#   requesting that we show whiskers the most extreme value at a
#   distance of at most 1x the IQR from the bottom and top edges of
#   the box plot.
#
# Again, we see that the towns' height distributions don't look all
# that different from one-another.  Generally, if the boxes of each
# distribution overlap, and you haven't taken something on the order
# of a buttload (metric units) of measurements, you should doubt the
# differenes in distribution averages.  It looks like a single height
# measurement for town 1 is pretty far away from the others, and you
# should investigate such measurements as potential outliers.
#
# ** Exercise ** Build a box-and-whiskers plot of the McCain and Obama
# campaign contributions.  Again, outliers make this a difficult task.  With *** whis=1 **, and by setting the y range of the plots like so

plt.set_ylim((-250, 1250))

# we got the following plot
#
# $$$
#
# Obama is on the left, and McCain on the right.  Man, real data sure
# is more confusing than fake data.  Obama's box plot is a lot tighter
# than McCains, who has a larger spread of donation sizes.  Both of
# Obama's whiskers are visible on this chart, whereas only the top
# whisker of McCain's plot is visible.  Another feature we haven't
# seen before is the stream of blue dots after each of the whiskers on
# each of Obama and McCain's plots.  These represent potential **
# outliers **, or values that are extreme and do not represent the
# majority of the dataset.
#
# It was easy to say that the histograms and box plots for the town
# heights overlapped heavily.  So while the effect size for town heights was pretty large, the distributions don't actually look all that different from one-another.
#
# The campaign plots are a bit harder to discern.  The histogram told us virtually nothing.  The box plot showed us that Obama's donations seemed more concentrated on the smaller end, whereas McCains seemed to span a larger range.  There was overlap between the boxes in the plot, but we don't really have a sense for just how much overlap or similarity there is between these distributions.  In the next section, we'll quantify the difference using statistics!
#
# <h5>Run a Statistical Test</h5>
#
# We have two population height averages.  We know that they are
# different, but charts show that overall the two towns look similar.
# We have two contribution averages that are also different, but with
# a murkier story after looking at our box-and-whisker plots.
#
# In statistics, what we are asking is whether differences we observed
# are reliable indicators of some trend, or just happened by lucky
# chance. For example, we might simply have measured particularly
# short members of town 1 and tall members of town 2.  ** Statistical
# significance ** is a measure of the probability that, for whatever
# reason, we stumbled upon the results we did by chance.
#
# There are several tests for statistical significance, each applying
# to a different question.  Our question is: "Is the difference in
# averages between the height of people in town 1 and town 2
# statistically significant?"  We ask a similar question about the
# difference in averages in campaign contributions.  The test that
# answers this question is the [T-Test]($$$).
#



# The T-Test has several flavors.  If your data is ** paired **, for
# example if you are measuring the performance of the same set of
# students on an exam before and after teaching them the content, you
# can run a paired T-Test.  In our case, our data is ** unpaired **.
# Another question is whether we have reason to believe that the two
# distributions have the same variance (a measure of the varition
# between measurements).  In our case, we have no way of knowing what
# the water treatment did to our distributions, so we'll be
# conservative.  We're going to un an unpaired T-Test on datasets of
# potentially unequal variance called ** Welch's T-Test **.
#
#
#
#
"""statistical significance is a thing (very short desc)
t test measures differences in avgs.
let's to welches
it wasn't significant

is there sucha  thing as "very" significant? no.  there is big effect size.
paired, unpaired, unequal variance
t-test assumptions
"""


import welchttest

print "Welch's T-Test p-value:", welchttest.ttest(town1_heights, town2_heights)

#
# WHAT!?!  T-TESTS CAN BE CALCULATED IN A SINGLE LINE OF PYTHON?  WHY DID IT TAKE SO LONG TO GET HERE!?!?!
#
# Hold on there, buddy.  We did a lot more than run a T-Test so far.
# We looked at an effect size that made us think the two population
# heights were different.  Then we built a boxplot that changed our
# viewpoint: the two populations, save a potential outlier, are not
# that different.  And, at the end of a long road, we are simply
# confirming what our eyes told us.
#
# The Welch's T-Test emitted a p-value of $$$.  The p-value is the
# probability that the measurements we saw in the two towns made us
# see an effect size that happened by chance.  In this case, there's
# $$$% chance that we've arrived at our effect size by chance.  What's
# a good cutoff?  Two popular values are .05 or .01: if there is less
# than a 5% or 1% chance that we arrived at our answer by chance,
# we're willing to say that we have a ** statistically significant **
# result.
#
# So in our case, our result is not significant.  Had we taken more
# measurements, or if the differences in heights were farther apart,
# we might have reached significance.  But, given our current results,
# let's not jump to conclusions.  After all, it was just food coloring
# in the water!
#
# <h5>Can You Have a Very Significant Result?</h5> No.  There aren't
# shades of significance!  You either believe that the effect size
# you're believing is a legitimate one, or you can't trust it to have
# been more than chance.  While people disagree about whether a
# p-value of .05 or .01 is required, they all agree that significance
# is a binary value.

#
# <h5>We Swept a Few Things Under The Rug/h5>
# 
# Tests for normality.  Mann-Whitney U Test.  Blah
# <h3>Campaign Contribution Sizes </h3>
#
# Now it's your turn!
#   * Using [LINK TO FILE](), Calculate the mean and standard
# deviation of the Obama and McCain campaign contributions.
#   * Then draw a box plot of each set of contributions.
#   * Run a the Shapiro-Wilk test on the data to see if it's
#   normal. Is it?
#   * Run the appropriate test (Welch's T or Mann-Whitney U).  Are the
# two averages different from one-another?

#http://hackingmedicine.mit.edu/conference/data-sources/



