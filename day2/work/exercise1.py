#!/usr/bin/env python

# Histogram of donations to each candidate

import collections, sys, csv, datetime, operator, math
import matplotlib.pyplot as p
import numpy as n


_spacing = 100;

def parse_contrib(file, ranges):
    """Parse out contributions of candidates from a file.
    
    Returns a dictionary of lists of date-amount tuples."""

    # Make as many default-counting dictionaries as there are candidates
    contribs = {}
    for candidate, range in ranges.iteritems():
        contribs[candidate] = \
            [0] * int(math.ceil((range[1] - range[0])/float(_spacing)) + 1)

    # CSV-parse the file
    reader = csv.DictReader(file)

    for row in reader:
        name = row['cand_nm']
        amount = float(row['contb_receipt_amt'])

        valid_names = [cname for cname in ranges.iterkeys() if cname in name]
        key = any(valid_names) and valid_names[0]

        # If candidates given and no match, key = False
        if key and \
           ranges[key][0] <= amount <= ranges[key][1]:

            # bin the amount by candidate
            bin = int(math.floor((amount - ranges[key][0]) / _spacing))
            contribs[key][bin] += 1 # Normal contributions

    return contribs

def setup_plot():
    """Create an empty 10x5 inch plot."""

    return p.figure(figsize=(10, 5))

    
    
def plot_hist(subplot, contribs, ranges):
    """Unpack and plot a candidate's contributions, with a label."""

    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown']
    width = _spacing

    ix = 0
    for candidate in contribs.iterkeys():
        left_edges = n.arange(ranges[candidate][0],
                              ranges[candidate][1] + width,
                              width) + \
                     (ix * width/2)
        subplot.bar(
            left_edges,
            contribs[candidate],
            width = width/2,
            color = colors[ix % len(colors)],
            linewidth = 0,
            label = candidate)

        ix += 1

def save_plot(candidates):
    """Make a legend and save the file with an identifying name."""

    root = 'contributions_by_size-'

    if candidates:
        name = root + \
               '_'.join([candidate.lower() for candidate in candidates]) + \
               '.png'
    else:
        name = root + 'all.png'

    p.legend(loc='best', ncol=2)
    p.savefig(name, format='png')

def plot_candidates(filename, ranges):
    """Given a filename and a list of candidates and contribution ranges, 
       turn it into a plot."""

    with open(filename) as file:
        contribs = parse_contrib(file, ranges)

        fig = setup_plot()
        subplot = fig.add_subplot(111)
        plot_hist(subplot, contribs, ranges)
        save_plot(contribs.keys())

def main():
    """Plot all candidates for the first given filename."""
    plot_candidates(
        sys.argv[1],
        {'Obama': (-18000, 19000), 'McCain': (-22000, 22000)})

if __name__ == '__main__':
    main()
