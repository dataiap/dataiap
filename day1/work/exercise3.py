#!/usr/bin/env python

# Candidates' cumulative reattributions to spouse by date

import collections, sys, csv, datetime, operator
import matplotlib.pyplot as p

_REATTRIB_TEXT = 'reattribution to spouse'

def parse_contrib(file, *candidates):
    """Parse out contributions of candidates from a file.
    
    Returns a dictionary of lists of date-amount tuples."""

    # Make as many default-counting dictionaries as there are candidates
    contribs = collections.defaultdict(
            lambda: collections.defaultdict(lambda: 0))

    contribs_cum = {}

    # CSV-parse the file
    reader = csv.DictReader(file)

    for row in reader:
        name = row['cand_nm']
        amount = float(row['contb_receipt_amt'])
        date = datetime.datetime.strptime(row['contb_receipt_dt'], '%d-%b-%y')


        # Filter by reattribution
        reattribution = _REATTRIB_TEXT in row['receipt_desc'].lower() or \
                        _REATTRIB_TEXT in row['memo_text'].lower()

        if reattribution and amount < 0:
            # No candidates => any candidate
            # Some candidates => do any of the candidate arguments match? 
            #                    if so, return the last one; else, false 
            key = (len(candidates) == 0 and name) or \
                  reduce(operator.or_, 
                         (cname for cname in candidates if cname in name),
                         False)

            # If candidates given and no match, key = False
            if key:
                contribs[key][date] -= amount # Need to compensate for negatives

    # Sort each candidate by date
    for (candidate, contrib) in contribs.iteritems():
        contribs_cum[candidate] = sorted(contrib.items())

    # Calculate cumulative contributions
    for candidate_contrib in contribs_cum.itervalues(): # For every candidate's contributions

        # Make a cumulative sum of the total contributions
        sum = 0
        for (ccx, contrib) in enumerate(candidate_contrib):
            sum += contrib[1]
            candidate_contrib[ccx] = (contrib[0], sum)

    return contribs_cum

def setup_plot():
    """Create an empty 10x5 inch plot."""

    return p.figure(figsize=(10, 5))

def plot_line(line_data, candidate):
    """Unpack and plot a candidate's contributions, with a label."""

    if len(line_data) > 1: # Don't plot empty lines
        x_data, y_data = zip(*line_data)
        p.plot(x_data, y_data, label = candidate)

def save_plot(candidates):
    """Make a legend and save the file with an identifying name."""

    root = 'reattribution_to_spouse_by_date-'

    if candidates:
        name = root + \
               '_'.join([candidate.lower() for candidate in candidates]) + \
               '.png'
    else:
        name = root + 'all.png'

    p.legend(loc='best', ncol=2)
    p.savefig(name, format='png')

def plot_candidates(filename, *candidates):
    """Given a filename and a list of candidates, turn it into a plot."""

    with open(filename) as file:
        contribs = parse_contrib(file, *candidates)

        setup_plot()
        for candidate, contrib in contribs.iteritems():
            plot_line(contrib, candidate)
        save_plot(candidates)

def main():
    """Plot all candidates for the first given filename."""
    plot_candidates(sys.argv[1])

if __name__ == '__main__':
    main()

