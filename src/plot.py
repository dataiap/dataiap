import random
import numpy as np
import matplotlib.pyplot as plt
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
fig = plt.figure(figsize=(50, 10))

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
# - subplot.set_ylabel()
# - subplot.set_xticks()
# - subplot.set_xticklabels()
# - subplot.set_yticks()
# - subplot.set_yticklabels()
#
#




#
# bar graphs http://matplotlib.sourceforge.net/api/axes_api.html#matplotlib.axes.Axes.bar
# left  - specifies the x coord of the left side of the bar.  The units are meaningless
#         because matplotlib internall computes the pixels to fit the subplot width
# width - used to specify the width of a bar, and the offset of the second bar. its value
#         is relative to the values in left. 
#
left = np.arange(len(xs))  * 2.0
width = 0.5

# note: add_subplot(xyz) means the figure is an x rows by y cols grid
#       and z is the subfigure within the grid (row first)
subplot = fig.add_subplot(221)
subplot.bar(left, ys, width, color=colors[0], linewidth=0)
subplot.bar(left+width, ys2, width, color=colors[1], bottom=ys, linewidth=0)



# line graphs
#
subplot = fig.add_subplot(222)
subplot.plot(xs, ys, xs, ys)


# boxplot graphs
#
# each boxdata contains the set of points to generate a single box
# the boxplot() method takes a list of boxdatas, and generates a box for each
# set of points.
#
subplot = fig.add_subplot(223)
boxdata1 = [random.randint(0, 20) for i in xrange(10)]
boxdata2 = [random.randint(20,40) for i in xrange(10)]
boxdata3 = [random.randint(40,60) for i in xrange(10)]
data = [boxdata1, boxdata2, boxdata3]
subplot.boxplot(data)
subplot.set_xlabel("some data")
subplot.set_title("My Boxplot")





plt.savefig('/tmp/test.png', format='png')
#plt.show()
