import random
import numpy
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
stds = [.001, 5, 20, 50, 100]

for idx, std in enumerate(stds):
    xs = range(100)
    #    ys = [random.gauss(x, std) for x in xs]
    ys = [random.gauss(5, std) for x in xs]
    subplot = fig.add_subplot(len(stds), 1, idx+1)
    subplot.scatter(xs, ys, color=colors[0])
    model = ols.ols(numpy.array(ys), numpy.array(xs), "y", "x")
    subplot.set_title("std = %f, R^2 = %f" % (std, model.R2))
    betas = model.b
    ps = model.p
    model_ys = [betas[0] + betas[1]*x for x in xs]
    attrs = lineattrs[1] if (ps[0] < .05 and ps[1] < .05) else lineattrs[2]
    print std, attrs, ps, model.R2
    subplot.plot(xs, model_ys, color=attrs[0], marker=attrs[1])
    #   print model.summary()
    #   print model.b, model.p
    
plt.savefig('/tmp/test.png', format='png')
#plt.show()
