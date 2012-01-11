#!/usr/bin/env python

import matplotlib.pyplot as p
import numpy as n
import random

random.seed(0)

fig = p.figure(figsize=(50,30))

N = 30
xx = n.arange(N)
y1 = [random.randint(0, 50) for ix in xx]
y2 = n.arange(N)

width = 0.25

subplot = fig.add_subplot(321)
subplot.bar(xx, y1, width = width)
subplot.bar(xx+width, y2, width = width, bottom = y1, color='#258f22')

subplot = fig.add_subplot(322)
subplot.plot(xx, y1, xx, y2)

subplot = fig.add_subplot(323)
boxdata = [[random.randint(0, random.randint(20, 60)) for ix in xrange(20)] \
           for ix in xrange(3)]
subplot.boxplot(boxdata)

subplot = fig.add_subplot(324)
subplot.scatter(xx, y1, marker = 'o', color='orange', linewidth=0)

import sys
sys.path.append('../../resources/util')
import map_util as m
import json


subplot = fig.add_subplot(325)
with open('../../datasets/geo/id-counties.json') as counties_file:
    counties = json.load(counties_file)
    for county in counties:
        m.draw_county(subplot, county)

subplot = fig.add_subplot(326)
with open('../../datasets/geo/id-states.json') as states_file:
    states = json.load(states_file)
    for state in states:
        m.draw_state(subplot, state)


p.show()
