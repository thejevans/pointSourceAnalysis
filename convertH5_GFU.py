#!/usr/bin/env python

'''
Template to convert from HDF5 files to NPY numpy array Files. This implementation uses
parseGFU.py to parse the data
'''

# Imports
from __future__ import print_function
from optparse import OptionParser
import tables
import numpy as np
import parseGFU

# Command parsing
usage = '%prog [options] --infile <hdf5 file> --outdir <output directory>'
parser = OptionParser(usage = usage, description=__doc__)
parser.add_option('-i', '--infile', type = 'string', default = None,
                  help = 'HDF5 file to be parsed')
parser.add_option('-o', '--outdir', type = 'string', default = './',
                  help = 'NPY file output path')
(options, args) = parser.parse_args()

inFile = options.infile
outDir = options.outdir

# If no input file given, ask for one
if inFile == None:
    inFile = raw_input('Select input HDF5 file: ')

# If output directory does not end with a /, add one
if outDir.rfind('/') != len(outDir)-1:
    outDir = ''.join([outDir, '/'])

# Set output file name based on input file name
outFile = ''.join([outDir, inFile[inFile.rfind('/')+1:inFile.rfind('.')], '.npy'])

# Read in .h5 file
hdf = tables.openFile(inFile)

# Convert to numpy array
arr = parseGFU.convert(hdf)

# Write out .npy file
np.save(outFile, arr)
