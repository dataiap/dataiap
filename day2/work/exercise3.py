#!/usr/bin/env python

# Candidates' reattributions to spouse scatterplot

import collections, sys, csv, datetime, operator
import matplotlib.pyplot as p

_REATTRIB_TEXT = 'reattribution to spouse'

def parse_contrib(file, *candidates):
    """Parse out contributions of candidates from a file.
    
    Returns a dictionary of lists of date-amount tuples."""

    # Make as many default-counting dictionaries as there are candidates
    reattribs = collections.defaultdict(
            lambda: [])

    # CSV-parse the file
    reader = csv.DictReader(file)

    for row in reader:
        name = row['cand_nm']
        amount = float(row['contb_receipt_amt'])
        date = datetime.datetime.strptime(row['contb_receipt_dt'], '%d-%b-%y')


        # Filter by reattribution
        reattribution = _REATTRIB_TEXT in row['receipt_desc'].lower() or \
                        _REATTRIB_TEXT in row['memo_text'].lower()

        # If candidates given and no match, key = False
        if reattribution and amount < 0:
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
                reattribs[key].append((date, -amount)) # Need to compensate for negatives

    
    return reattribs

def setup_plot():
    """Create an empty 10x5 inch plot."""
    return p.figure(figsize=(10, 5))

def color_scheme():
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown']
    ncolors = len(colors)
    ix = 0

    while(True):
        yield colors[ix % ncolors]
        ix += 1

def plot_contrib(contribs):
    """Unpack and plot a candidate's contributions, with a label."""

    colors = color_scheme()


    for candidate, contribs in contribs.iteritems():
        dates, amounts = zip(*contribs)
        p.scatter(
            dates,
            amounts,
            linewidth = 0,
            color = colors.next(),
            label = candidate)

def save_plot(*candidates):
    """Make a legend and save the file with an identifying name."""

    root = 'reattributions_scatter-'

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

        fig = setup_plot()
        plot_contrib(contribs)
        save_plot()

def main():
    """Plot all candidates for the first given filename."""
    plot_candidates(sys.argv[1])

if __name__ == '__main__':
    main()

