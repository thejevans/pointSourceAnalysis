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
from icecube import astro

# Function for polynomial pull correction
def pullCorrection (ang_err, logE, a, b, c, d, e, f):
    poly = lambda X: (a * X**5 + b * X**4 + c * X**3 + d * X**2 + e * X + f)
    return ang_err * poly(logE)

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
hdf  = tables.openFile(inFile)
f    = hdf.root
data = f.OnlineL2_SplineMPE.cols

# Build empty array for conversion
arr = np.empty(len(data.Event), dtype=[("run", np.int),
                                       ("event", np.int),
                                       ("azimuth", np.float),
                                       ("zenith", np.float),
                                       ("time_mjd", np.float),
                                       ("logE", np.float),
                                       ("ra", np.float),
                                       ("dec", np.float),
                                       ("para_ang_err", np.float),
                                       ("boot_ang_err", np.float),
                                       ("cr_ang_err", np.float)])

# Copy needed data to array
arr["run"]          = data.Run[:]
arr["event"]        = data.Event[:]
arr["azimuth"]      = data.azimuth[:]
arr["zenith"]       = data.zenith[:]
arr["time_mjd"]     = f.I3EventHeader.cols.time_start_mjd[:]
arr["logE"]         = np.log10(f.OnlineL2_SplineMPE_MuEx.cols.energy[:])
arr["boot_ang_err"] = f.OnlineL2_SplineMPE_Bootstrap_Angular.cols.value[:]

# Convert to RA and Dec from zenith, azimuth, and time and add to array
arr["ra"], arr["dec"] = astro.dir_to_equa(arr["zenith"],
                                          arr["azimuth"],
                                          arr["time_mjd"])

# Compute paraboloid sigma and add to array
para_zenith_err     = f.OnlineL2_SplineMPE_ParaboloidFitParams.cols.err1[:]
para_azimuth_err    = f.OnlineL2_SplineMPE_ParaboloidFitParams.cols.err2[:]
arr["para_ang_err"] = np.sqrt((para_zenith_err**2 + para_azimuth_err**2) / 2)

# Compute Cramer-Rao sigma and add to array
cr_zenith_err     = f.OnlineL2_SplineMPE_CramerRao_cr_zenith[:]['value']
cr_azimuth_err    = f.OnlineL2_SplineMPE_CramerRao_cr_azimuth[:]['value']
arr["cr_ang_err"] = np.sqrt((cr_zenith_err**2 + (cr_azimuth_err
                            * np.sin(arr["zenith"]))**2) / 2)

# Define factor to convert from 50% error circle to 1-sigma error circle
OneSigmaFactor = 1 / 1.144

# Apply pull corrections
arr["para_ang_err"] = OneSigmaFactor * pullCorrection(arr["para_ang_err"],
                                                      arr["logE"],
                                                      a=3.13000733,
                                                      b=-18.48507616,
                                                      c=38.57383162,
                                                      d=-28.36630035,
                                                      e=-7.04750628,
                                                      f=18.80268337)
arr["boot_ang_err"] = OneSigmaFactor * pullCorrection(arr["boot_ang_err"],
                                                      arr["logE"],
                                                      a=-9.9904024,
                                                      b=96.01333438,
                                                      c=-365.5160818,
                                                      d=689.33042332,
                                                      e=-644.23193086,
                                                      f=240.64957472)
arr["cr_ang_err"]   = OneSigmaFactor * pullCorrection(arr["cr_ang_err"],
                                                      arr["logE"],
                                                      a=0.67265095,
                                                      b=-6.06121132,
                                                      c=23.49381922,
                                                      d=-47.00156442,
                                                      e=46.95473381,
                                                      f=-15.75197234)

# Decide which error estimate to use
threshold = np.log10(4e12)
for event in arr.T:
    event["para_ang_err"] *= event["logE"] < threshold
    event["boot_ang_err"] *= event["logE"] >= threshold
    event["cr_ang_err"]   *= event["para_ang_err"] == 0 and event["boot_ang_err"] == 0

# Write out .npy file
np.save(outFile, arr)
