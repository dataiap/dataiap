import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import regression
import ols
random.seed(0)

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
markers = [None, 'o', '+', 'x', 'D']
styles = ['-', '--']
lineattrs = [(color, m, s)  for s in styles for m in markers for color in colors ]

# setup the Figure
# figsize - (width, height) in inches
# 
fig = plt.figure(figsize=(50, 50))

# Scatterplot Graph
#
(ypll_arr, adtl_arr) = regression.get_arrs()
for idx, independent in enumerate(regression.independent):
    subplot = fig.add_subplot(5, 3, idx)
    subplot.scatter(adtl_arr[:,idx], ypll_arr, color=colors[0])
    subplot.set_title("%s vs. %s" % (independent, regression.dependent[0]))
    model = ols.ols(ypll_arr, adtl_arr[:, idx], regression.dependent[0], [independent])
    betas = model.b
    ps = model.p
    ys = [betas[0] + betas[1]*x for x in adtl_arr[:, idx]]
    attrs = lineattrs[1] if (ps[0] < .05 and ps[1] < .05) else lineattrs[2]
    print independent, attrs, ps, model.R2, model.R2adj
    subplot.plot(adtl_arr[:, idx], ys, color=attrs[0], marker=attrs[1])
    model.summary()
    #   print model.b, model.p
    print
    print
    print

    
plt.savefig('/tmp/test.png', format='png')
#plt.show()
