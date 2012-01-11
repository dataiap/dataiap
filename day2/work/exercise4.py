#!/usr/bin/env python

# Choropleths

import collections, sys, csv, datetime, operator, math
import matplotlib.pyplot as p
import numpy as n
sys.path.append('../../resources/util')
import map_util as m

_MAXDONATION = 0

def parse_contrib(file, *candidates):
    """Parse out contributions of candidates from a file.
    
    Returns a dictionary of dictionaries."""

    global _MAXDONATION

    # Make as many default-counting dictionaries as there are candidates
    contribs = collections.defaultdict(
            lambda: collections.defaultdict(lambda: 0))

    # CSV-parse the file
    reader = csv.DictReader(file)

    for row in reader:
        name = row['cand_nm']
        state = row['contbr_st']
        amount = float(row['contb_receipt_amt'])

        key = False

        if candidates: 
        # Some candidates => do any of the candidate arguments match? 
        #                    if so, return the last one; else, false 
            valid_names = [cname for cname in candidates if cname in name]
            key = any(valid_names) and valid_names[0]
        else:
        # No candidates => any candidate
            key = name
    
        if key:
            contribs[key][state] += amount

    # Calculate max and logs on a second pass to avoid needless calculation
    # make everything a log-scale to bring out the low-scoring candidates
    for contrib in contribs.itervalues():
        for state, amount in contrib.iteritems():
            if amount > 0:
                amount = math.log(amount)

            if amount < 0:
                amount = 0

            if amount > _MAXDONATION:
                _MAXDONATION = amount

            contrib[state] = amount

    return contribs

def setup_plot():
    """Create an empty 14x10 inch plot."""

    return p.figure(figsize=(18, 12))

    
def donation_color(donation):
    return m.blues[int(float(donation)/_MAXDONATION * (len(m.blues) - 1))]


def plot_contrib(contribs):
    """Unpack and plot candidates' contributions by state in different subplots"""

    rows = 4
    cols = math.ceil(len(contribs)/rows)

    pix = 0
    for candidate, contrib in contribs.iteritems():
        subplot = p.gcf().add_subplot(rows, cols, pix)

        for state, amount in contrib.iteritems():
            m.draw_state(subplot,
                         m.get_statename(state),
                         color = donation_color(amount))

        # Make it pretty
        subplot.set_title(candidate)
        subplot.set_xticks([])
        subplot.set_yticks([])

        pix += 1
        
def save_plot(*candidates):
    """Make a legend and save the file with an identifying name."""

    root = 'contributions_by_state-'

    if candidates:
        name = root + \
               '_'.join([candidate.lower() for candidate in candidates]) + \
               '.png'
    else:
        name = root + 'all.png'

    p.legend(loc='best', ncol=2)
    p.savefig(name, format='png')

def plot_candidates(filename, *candidates):
    """Given a filename and a list of candidates and contribution ranges, 
       turn it into a plot."""

    with open(filename) as file:
        contribs = parse_contrib(file, *candidates)

        setup_plot()
        plot_contrib(contribs)
        save_plot(*candidates)

def main():
    """Plot all candidates for the first given filename."""
    plot_candidates(sys.argv[1])
        

if __name__ == '__main__':
    main()
