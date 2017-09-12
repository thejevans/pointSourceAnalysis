#!/usr/bin/env python

'''

'''

from __future__ import print_function
from optparse import OptionParser
import numpy as np
from glob import glob
import injectEvents

# Command parsing
usage = '%prog [options] --indir <input directory> --outdir <output directory>'
parser = OptionParser(usage = usage, description=__doc__)
parser.add_option('-i', '--indir', type = 'string', default = '/data/i3store0/users/jevans96/point_source_analysis/distributed_outputs/data/',
                  help = 'Directory containing numpy files')
parser.add_option('-o', '--outdir', type = 'string', default = '/data/i3store0/users/jevans96/point_source_analysis/charts/',
                  help = 'Directory to output histogram')
(options, args) = parser.parse_args()

inDir = options.indir
outDir = options.outdir

# If input directory does not end with a /, add one
if inDir.rfind('/') != len(inDir)-1:
    inDir = ''.join([inDir, '/'])

# If output directory does not end with a /, add one
if outDir.rfind('/') != len(outDir)-1:
    outDir = ''.join([outDir, '/'])

# Get filenames
filenames = sorted(glob(''.join([inDir, '*.npy'])))
inFile    = filenames[0]

# Combine and save data
data = np.empty(0)

arr = np.load(filenames[0])[1]

for filename in filenames:
    data = np.append(data, np.load(filename)[0])

# Set output file name based on input file name
outFile = ''.join([outDir, 'TSD_{0}_Trials'.format(len(data)), '.png'])

np.save(''.join([outFile[:outFile.rfind('.')],'.npy']), data)

# plot
injectEvents.plotTSD(data, arr, outFile)
