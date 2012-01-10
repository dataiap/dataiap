#!/usr/bin/env python

# pyplot is the plotting module
import matplotlib.pyplot as plt
import random

# generate the data
xs = range(10) # 0...9
ys1 = range(10) # 0...9
ys2 = [random.randint(0, 20) for i in range(10)] # 10 random numbers from 0-19

# create a 10-inch x 5-inch figure
fig = plt.figure(figsize=(10,5))

# draw a line graph
plt.plot(xs, ys1, label='line 1')
plt.plot(xs, ys2, label='line 2')

# create the legend
plt.legend(loc='upper center', ncol = 4)

# finally, render and store the figure in an image
plt.savefig('twolines.svg', format='svg')

