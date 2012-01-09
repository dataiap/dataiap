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

figure = plt.figure(figsize=(15, 20))
subplot = figure.add_subplot(211)

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
subplot.set_title("rappers born per county.  darker means more rappers")
subplot.set_xlim(-150, -50)
subplot.set_ylim(15, 70)


subplot = figure.add_subplot(212)

reader = csv.DictReader(open('../county_health_rankings/ypll.csv', 'r'))
for row in reader:
    if 'County' not in row:
        continue
    if not row['YPLL Rate']    :
        continue
    fips = int(row['FIPS'])
    ypll = float(row['YPLL Rate'])

    count = float(counts.get(fips, 0.0))
    subplot.scatter(count, ypll, color=blues[8])

subplot.set_xlabel("# Rappers in County")
subplot.set_ylabel("YPLL Rate")
figure.savefig('/tmp/rap.png', format='png')

