#!/usr/bin/env python

"""
Converts HDF5 Files from the GFU sample to a numpy array file. Uses Cramer-Rao
method for determining angular error. This method requires a pull correction due
to artificial results from higher energies. In order to get a 1-sigma error on
RA and Dec, I used the fit for (Cramer-Rao, Spline MPE, 50%). This pull
correction is then divided by 1.144 to get a 39% error circle, which corresponds
to a 1-sigma error. This factor assumes a 2-D Gaussian distribution, and will
need to be altered if you want to use a Kent distribution.

Resources:
https://wiki.icecube.wisc.edu/index.php/IC-40_CramerRao_Comparison
https://wiki.icecube.wisc.edu/index.php/Optical_Follow-Up_Pull_Correction_2016
"""

# Imports
from __future__ import print_function
from optparse import OptionParser
import tables
import numpy as np
import parseGFU

# Command parsing
usage = "%prog [options] --infile <hdf5 file> --outdir <output directory>"
parser = OptionParser(usage = usage, description=__doc__)
parser.add_option("-i", "--infile", type = "string", default = None,
                  help = "HDF5 file to be parsed")
parser.add_option("-o", "--outdir", type = "string", default = './',
                  help = "NPY file output path")
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
outFile = ''.join([outDir,
                   inFile[inFile.rfind('/')+1:inFile.rfind('.')],
                   '.npy'])

# Read in .h5 file
hdf = tables.openFile(inFile)

# Convert to numpy array
arr = parseGFU.convert(hdf)

# Write out .npy file
np.save(outFile, arr)
