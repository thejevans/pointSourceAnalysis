from __future__ import print_function
import tables
import numpy as np
from icecube import astro

def convert (hdf):
    '''
    Converts HDF5 Files from the GFU sample to a numpy array file. Uses Cramer-Rao method
    for determining angular error, which requires a pull correction due to artificial
    results from higher energies. In order to get a 1-sigma error on RA and Dec, I used
    the pull correction formula for 50% contained probability and divided by 1.144 to get
    a 39% error circle, which corresponds to a 1-sigma error. This factor assumes a 2-D
    Gaussian distribution, and will need to be altered if you want to use a Kent
    distribution.

    Resources:
    https://wiki.icecube.wisc.edu/index.php/IC-40_CramerRao_Comparison
    https://wiki.icecube.wisc.edu/index.php/Optical_Follow-Up_Pull_Correction_2016
    '''
    f    = hdf.root
    data = f.OnlineL2_SplineMPE.cols

    # Build empty array for conversion
    arr = np.empty(len(data.Event), dtype=[('run', np.int),
                                           ('event', np.int),
                                           ('azimuth', np.float),
                                           ('zenith', np.float),
                                           ('time_mjd', np.float),
                                           ('logE', np.float),
                                           ('ra', np.float),
                                           ('dec', np.float),
                                           ('ang_err', np.float)])

    # Copy needed data to array
    arr['run']      = data.Run[:]
    arr['event']    = data.Event[:]
    arr['azimuth']  = data.azimuth[:]
    arr['zenith']   = data.zenith[:]
    arr['time_mjd'] = f.I3EventHeader.cols.time_start_mjd[:]
    arr['logE']     = np.log10(f.OnlineL2_SplineMPE_MuEx.cols.energy[:])

    # Convert to RA and Dec from zenith, azimuth, and time and add to array
    arr['ra'], arr['dec'] = astro.dir_to_equa(arr['zenith'], arr['azimuth'], arr['time_mjd'])

    # Compute Cramer-Rao sigma and add to array
    zenith_err     = f.OnlineL2_SplineMPE_CramerRao_cr_zenith[:]['value']
    azimuth_err    = f.OnlineL2_SplineMPE_CramerRao_cr_azimuth[:]['value']
    arr['ang_err'] = np.sqrt((zenith_err**2 + (azimuth_err * np.sin(arr['zenith']))**2) / 2)

    # Define factor to convert from 50% error circle to 1-sigma error circle
    oneSigmaFactor = 1 / 1.144

    # Apply pull correction and conversion to 1-sigma (if pull correction gives a value
    # less than 1, make it 1 instead)
    pull_coeff      = [0.03662, -0.70540, 5.38363, -19.84729, 34.88499, -22.33384]
    pull_corr       = np.polyval(pull_coeff, arr['logE'])
    arr['ang_err'] *= oneSigmaFactor * np.array([1 if x < 1 else x for x in pull_corr])

    return arr
