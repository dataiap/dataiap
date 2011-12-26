import random, json, sys
import numpy as np
import matplotlib.pyplot as plt
from util.map_util import *
from collections import defaultdict
from matplotlib.patches import Rectangle
random.seed(0)



colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
	  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
markers = [None, 'o', '+', 'x', 'D']
styles = ['-', '--']
lineattrs = [(color, m, s)  for s in styles for m in markers for color in colors ]

N = 100
xs = range(N)
ys = [random.randint(0, 50) for i in xs]
ys2 = range(N)


#
# setup the Figure
# figsize - (width, height) in inches
# 
fig = plt.figure(figsize=(50, 30))

#
# the figure is the container that our plots will be drawn in
# each plot (chart) will be individually added using *figure.add_subplot()*
# 
# the subplot will be our unit of charting.  a subplot object (called an Axes in matplotlib)
# has many functions to add objects (bars, lines, legends etc) to the subplot.  
# some useful functions to make charts include:
#
# - subplot.bar(lefts, heights, width=?, bottom=None)
# - subplot.boxplot()
# - subplot.errorbar() - plot points with error bars
# - subplot.plot() - plot x,y pairs with custom lines and markers
# - subplot.loglog()
# - subplot.semilogx()
# - subplot.semilogy()
# - subplot.scatter(xs, ys, s=15) - scatterplot. s stands for size
#
# The following are some useful keyword args that many of the above functions accept:
# 
# - linewidth=[None | number] - width of line. None for default
# - color=[string] - HTML (#ffffff), or common names ('red', 'green') work
# - xerr=[list] - list of floats that specify x-axis error bars
# - yerr=[list] - list of floats that specify y-axis error bars
#
# There are also functions to draw polygons
#
# - subplot.fill()
# - subplot.text()
#
# Some useful auxiliary functions include:
#
# - subplot.clear() - clear all the objects on the subplot
# - subplot.legend() - add a legend
# - subplot.set_title()
# - subplot.set_xlabel()
# - subplot.set_xticks()
# - subplot.set_xticklabels()
# - subplot.set_xscale() - 'linear'/'log'/'symlog'
# - subplot.set_ylabel()
# - subplot.set_yticks()
# - subplot.set_yticklabels()
# - subplot.set_yscale()
#




# bar graphs
# http://matplotlib.sourceforge.net/api/axes_api.html#matplotlib.axes.Axes.bar
#
# left  - specifies the x coord of the left side of the bar.  The units are meaningless
#         because matplotlib internall computes the pixels to fit the subplot width
# width - used to specify the width of a bar, and the offset of the second bar. its value
#         is relative to the values in left. 
#
left = np.arange(len(xs))  * 2.0
width = 0.5

# note: add_subplot(x,y,z) means the figure is an x rows by y cols grid
#       and z is the subfigure within the grid (row first)
# note: add_subplot(xyz) is a shorthand when x,y,z are single digits
subplot = fig.add_subplot(321)
subplot.bar(left, ys, width, color=colors[0], linewidth=0)
subplot.bar(left+width, ys2, width, color=colors[1], bottom=ys, linewidth=0)
subplot.set_title("Bargraph Example")



# line graphs
# http://matplotlib.sourceforge.net/api/axes_api.html#matplotlib.axes.Axes.plot
# 
subplot = fig.add_subplot(322)
# shorthand for:
#   subplot.plot(xs, ys)
#   subplot.plot(xs, ys2)
subplot.plot(xs, ys, xs, ys2)
subplot.set_title("Line graph/plot Example")


# boxplot graphs
# http://matplotlib.sourceforge.net/api/axes_api.html#matplotlib.axes.Axes.plot
#
# each boxdata contains the set of points to generate a single box
# the boxplot() method takes a list of boxdatas, and generates a box for each
# set of points.
#
subplot = fig.add_subplot(323)
boxdata1 = [random.randint(0, 20) for i in xrange(10)]
boxdata2 = [random.randint(20,40) for i in xrange(10)]
boxdata3 = [random.randint(40,60) for i in xrange(10)]
data = [boxdata1, boxdata2, boxdata3]
subplot.boxplot(data)
subplot.set_title("Boxplot Example")


# Scatterplot Graph
# http://matplotlib.sourceforge.net/api/axes_api.html#matplotlib.axes.Axes.plot
#
# 
subplot = fig.add_subplot(324)
subplot.scatter(xs, ys, color=colors[0])
# size (s keyword arg) varies with ys2
subplot.scatter(xs, ys2,color=colors[1],s=ys2)
subplot.set_title("Scatterplot Example")

#########################
# Geographical Graph
#########################


# Plot by County
#
subplot = fig.add_subplot(325)
data = json.load(file('../datasets/geo/id-counties.json'))
for fips in data:
    draw_county(subplot, fips)
subplot.set_title("Counties Example")
subplot.set_xlim(-200, -50)
subplot.set_ylim(15, 80)

# State Graph
#
subplot = fig.add_subplot(326)
data = json.load(file('../datasets/geo/id-states.json'))
for state in data:
    draw_state(subplot, state)
subplot.set_title("States Example")
subplot.set_xlim(-200, -50)
subplot.set_ylim(15, 80)




plt.savefig('/tmp/test.png', format='png')
#plt.show()
