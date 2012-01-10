#!/usr/bin/env python

# Candidates' contributions by date

import collections, sys, csv, datetime, operator
import matplotlib.pyplot as p

def parse_contrib(file, *candidates):
    """Parse out contributions of candidates from a file.
    
    Returns a list of lists of date-amount tuples."""

    # Make as many default-counting dictionaries as there are candidates
    num_candidates = len(candidates)

    # Make deep copies!
    contribs = [collections.defaultdict(lambda: 0) for ix in xrange(num_candidates)]

    contribs_by_date = []

    # CSV-parse the file
    reader = csv.DictReader(file)

    for row in reader:
        name = row['cand_nm']
        amount = float(row['contb_receipt_amt'])
        date = datetime.datetime.strptime(row['contb_receipt_dt'], '%d-%b-%y')

        for (ix, candidate) in enumerate(candidates):
            if candidate in name:
                contribs[ix][date] += amount

    # Sort each candidate by date
    for contrib in contribs:
        contribs_by_date.append(
            sorted(contrib.items(),
                   key=operator.itemgetter(0)))

    return contribs_by_date

def setup_plot():
    """Create an empty 10x5 inch plot."""

    return p.figure(figsize=(10, 5))

def plot_line(line_data, candidate):
    """Unpack and plot a candidate's contributions, with a label."""
    x_data, y_data = zip(*line_data)
    p.plot(x_data, y_data, label = candidate)

def save_plot(candidates):
    """Make a legend and save the file with an identifying name."""
    name = 'contributions_by_date-' + \
           '_'.join([candidate.lower() for candidate in candidates]) + \
           '.png'
    p.legend(loc='upper center', ncol = 4)
    p.savefig(name, format='png')

def plot_candidates(filename, *candidates):
    """Given a filename and a list of candidates, turn it into a plot."""
    with open(filename) as file:
        contribs = parse_contrib(file, *candidates)

        setup_plot()
        for contrib, candidate in zip(contribs, candidates):
            plot_line(contrib, candidate)
        save_plot(candidates)

def main():
    """Plot Obama and McCain for the first given filename."""
    plot_candidates(sys.argv[1], 'Obama', 'McCain')

if __name__ == '__main__':
    main()

