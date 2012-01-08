import freebase, json, sys, csv
sys.path.append('../../resources/util')
from map_util import *
from collections import Counter
import matplotlib.pyplot as plt

reader = csv.DictReader(open('rapper_counts.csv', 'r'))

counts = {}
for row in reader:
    try:
        counts[int(row['fips'])] = int(row['count'])
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

subplot.set_xlim(-150, -50)
subplot.set_ylim(15, 70)
        
figure.savefig('/tmp/rap.png', format='png')

