import freebase, json, sys, csv
sys.path.append('../../resources/util')
sys.path.append('../../day3/')
from map_util import *
from collections import Counter
import matplotlib.pyplot as plt
import ols
import numpy as np


reader = csv.DictReader(open('rapper_counts.csv', 'r'))

counts = {}
for row in reader:
    try:
        counts[row['fips']] = int(row['count'])
    except:
        pass


maxcount = 0.0
for fips, c in counts.iteritems():
    if fips:
        maxcount = max(maxcount, c)

figure = plt.figure(figsize=(15, 10))
subplot = figure.add_subplot(111)

breaks = []
div = maxcount
for i in xrange(len(blues)):
    breaks.append(div)
    div /= 2.0
breaks.sort()

for fips, c in counts.iteritems():
    if fips:
        for idx, b in enumerate(breaks):
            if c <= b:
                draw_county(subplot, fips, color=blues[idx])
                break
subplot.set_title("rappers born per county.  darker means more rappers", size=30)
subplot.set_xlim(-150, -50)
subplot.set_ylim(15, 70)


for tick in subplot.xaxis.get_major_ticks():
    tick.label1.set_fontsize(19)
for tick in subplot.yaxis.get_major_ticks():
    tick.label1.set_fontsize(19)
figure.savefig('./rap_map.png', format='png')




figure.clear()
subplot = figure.add_subplot(111)

reader = csv.DictReader(open('../county_health_rankings/ypll.csv',
                             'r'))
l_ypll = []
l_rapper = []
for row in reader:
    if 'County' not in row:
        continue
    if not row['YPLL Rate']:
        continue
    fips = row['FIPS']
    ypll = float(row['YPLL Rate'])

    if fips not in counts:
        continue

    count = float(counts.get(fips, 0.0))
    subplot.scatter(count, ypll, color=blues[8], alpha=0.4)
    l_ypll.append(ypll)
    l_rapper.append(counts.get(fips))


print np.array(l_ypll).shape, np.array(l_rapper).shape



model = ols.ols(np.array(l_ypll), np.array(l_rapper), "YPLL Rate", ["rappers"])
model.summary()

for tick in subplot.xaxis.get_major_ticks():
    tick.label1.set_fontsize(19)
for tick in subplot.yaxis.get_major_ticks():
    tick.label1.set_fontsize(19)


subplot.set_xlabel("# Rappers in County", size=30)
subplot.set_ylabel("YPLL Rate", size=30)
figure.savefig('./rap_scatter.png', format='png')



# caroline





