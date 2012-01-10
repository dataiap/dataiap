#!/usr/bin/env python

# Candidates' cumulative reattributions to spouse as fraction of cumulative
# contributions by date

import collections, sys, csv, datetime, operator
import matplotlib.pyplot as p

_REATTRIB_TEXT = 'reattribution to spouse'

def parse_contrib(file, *candidates):
    """Parse out contributions of candidates from a file.
    
    Returns a dictionary of lists of date-amount tuples."""

    # Make as many default-counting dictionaries as there are candidates
    contribs = collections.defaultdict(
            lambda: collections.defaultdict(lambda: 0))

    reattribs = collections.defaultdict(
            lambda: collections.defaultdict(lambda: 0))

    reattribs_cum = collections.defaultdict(lambda: {})
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

        # No candidates => any candidate
        # Some candidates => do any of the candidate arguments match? 
        #                    if so, return the last one; else, false 
        key = (len(candidates) == 0 and name) or \
              reduce(operator.or_, 
                     (cname for cname in candidates if cname in name),
                     False)

        # If candidates given and no match, key = False
        if key:
            contribs[key][date] += amount # Normal contributions

            if reattribution and amount < 0:
                reattribs[key][date] -= amount # Need to compensate for negatives

    # Sort each candidate by date
    # No need to sort the reattributions yet, since they are most useful
    # as a default dictionary right now anyway: if we were to replace it with
    # a sorted list of items, the contributions and reattributions would have
    # a different number of elements in them. We'd rather just sort the
    # contributions, since they are at least as frequent as reattributions and
    # will need to be sorted anyway to calculate the sum. Then, we can ask for
    # the reattributions as necessary
    for candidate in contribs.iterkeys():
        contribs_cum[candidate] = sorted(contribs[candidate].items())

    # Calculate cumulative contributions, reattributions, and ratios
    for (candidate, candidate_contribs) in contribs_cum.iteritems(): 
        # For every candidate's contributions

        # Make a cumulative sum of the total contributions
        contrib_sum = 0
        reattrib_sum = 0

        for (ccx, contrib) in enumerate(candidate_contribs):
            contrib_date = contrib[0]

            contrib_amount = contrib[1]
            reattrib_amount = reattribs[candidate][contrib_date]

            contrib_sum += contrib_amount
            reattrib_sum += reattrib_amount

            reattribs_cum[candidate][contrib_date] = float(reattrib_sum)/contrib_sum
            reattribs_cum[candidate][contrib_date] 

    # Now that all the relative reattributions have been calculated, we can
    # sort the list, since it has the appropriate number of elements in it
    for candidate in reattribs_cum.keys(): # not iterkeys due to deletion
        reattribs_cum[candidate] = sorted(reattribs_cum[candidate].items())

        # Remove empty candidates
        if reattribs_cum[candidate][-1][1] <= 0.0:
            del reattribs_cum[candidate]
    
    return reattribs_cum

def setup_plot():
    """Create an empty 10x5 inch plot."""

    return p.figure(figsize=(10, 5))

def plot_line(line_data, candidate):
    """Unpack and plot a candidate's contributions, with a label."""

    if len(line_data) > 0: # Don't plot empty lines
        x_data, y_data = zip(*line_data)
        p.plot(x_data, y_data, label = candidate)

def save_plot(candidates):
    """Make a legend and save the file with an identifying name."""

    root = 'reattribution_to_spouse_by_date_relative-'

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

