#!/usr/bin/env python

import sys

# Resample
with open(sys.argv[1], 'r') as file: 
    ix = 0
    for line in file:
        if ix % 500 == 0:
            print line,
        ix += 1

