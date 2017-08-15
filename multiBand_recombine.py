#!/usr/bin/env python

'''

'''

from __future__ import print_function
from optparse import OptionParser
import numpy as np
from glob import glob
import getBackground

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
arr = np.load(inFile)
data = np.empty(len(arr[0]['bandWidth']), dtype = [('bandWidth', np.float),('TSD', np.int, len(arr[0]['TSD'][0]))])
data['bandWidth'] = arr[0]['bandWidth']

for filename in filenames:
    for i, TSD in enumerate(np.load(filename)[0]['TSD']):
        data['TSD'][i] = np.append(data['TSD'][i], TSD[i])

# Set output file name based on input file name
outFilename = ''.join([outDir, 'multiBand_TSD_{0}_Trials'.format(len(data))])
np.save('.'.join([outFilename,'npy']), data)

# plot
for i, band in enumerate(arr[0]['bandWidth']):
    getBackground.plotTSD(data['TSD'][i], arr[1], '.'.join([outFilename, 'band_{0}'.format(i), 'png']), bandWidth = band)
