#!/usr/bin/env python

# On our first day, we loaded campaign contribution data and plotted
# it in different ways.  Today, we'll statistically compare parts of
# this dataset.  We'll also use another dataset (the [County Health
# Ranking]($$$)) to identify ways to predict mortality rates across
# the United States.
#
# <h3>Comparing means using T-Tests</h3>
#
# One thing that's been claimed about the 2008 election is that
# President Obama raised smaller quantities from a larger group of
# donors than Senator McCain, who raised a smaller number of large
# contributions.  Statistical techniques will help us determine how
# true this statement is.
#
# Whenever you have a hunch (a **hypothesis** in statistician-speak),
# the first thing to do is to look at some summary statistics (e.g.,
# averages), and explore the data graphically.  Let's install two
# useful packages for numerical computation and scientific computing:
#
#     sudo pip install numpy
#     sudo pip install scipy
#
# Let's try our hypothesis-testing chops using a toy example: two
# identical communities, that only differ in that one of the
# communities had "something in the water" the year a bunch of kids
# were born.  Did that something in the water affect the height of
# these kids?  (Note: this situation is not realistic.  it's never the
# case that the only difference between two communities is the one you
# want to measure, but it's a nice goal!) Let's look at some summary
# statistics.

import numpy
town1_heights = [5, 6, 7, 6, 7.1, 6, 4]
town2_heights = [5.5, 6.5, 7, 6, 7.1, 6]

town1_mean = numpy.mean(town1_heights)
town2_mean = numpy.mean(town2_heights)

print "Town 1 avg. height", town1_mean
print "Town 2 avg. height", town2_mean

print "Effect size: ", abs(town1_mean - town2_mean)

# It looks like town 2's average height (6.35 feet) is higher than
# town 1 (5.16$$$ feet) by a difference of 1.19$$$ feet.  This difference is
# called the ** Effect size **.  Town 2 certainly looks taller than
# Town 1!  Before we fire up the presses, let's see if we can confirm
# a statistical difference in distributions.
# 
# The first thing we'll do is plot the data in a box plot.  This will
# enable us to compare how much these two distributions will overlap.
# If the two towns really are of different heights, we'll see that the
# height distributions don't overlap.
#

import matplotlib.pyplot as plt

fig = plt.figure()
sub = fig.add_subplot(111)
sub.boxplot([town1_heights, town2_heights])
plt.show()

# 


# 
#
# <h3>Campaign Contribution Sizes </h3>
#
# 
# ** Exercise **: Now it's your turn.
#
#   * Using [LINK TO FILE](), Calculate the mean and standard
# deviation of the Obama and McCain campaign contributions.
#   * Then draw a box plot of each set of contributions.
#   * Run a the Shapiro-Wilk test on the data to see if it's
#   normal. Is it?
#   * Run the appropriate test (Welch's T or Mann-Whitney U).  Are the
# two averages different from one-another?





