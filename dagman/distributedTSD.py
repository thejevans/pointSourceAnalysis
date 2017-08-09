#!/usr/bin/env python
from __future__ import print_function
from optparse import OptionParser
import numpy as np

import time, socket
print ('########################################################################################')
print ('#### This job is running on {0}'.format(socket.gethostname()))
print ('########################################################################################')
print (' ')

# parsing options/params
usage = "usage: %prog [options]"
parser = OptionParser(usage = usage)

parser.add_option("-i", "--infile", type = "string",
                  default = '/data/i3store0/users/jevans96/point_source_analysis/converted_point_source_data/Data.2015.29652698sec.npy',
                  help = "address of your output file")
parser.add_option("-o", "--outfile", type = "string",
                  default = '/data/i3store0/users/jevans96/point_source_analysis/distributed_outputs/data/outfile.npy',
                  help = "address of your input file")
parser.add_option("-t", "--iter", type = "int",
                  default = 10,
                  help = "number of iterations")
parser.add_option("-v", "--verbose", action = "store_true",
                  default = False,
                  help = "print out if true")
(options, args) = parser.parse_args()

iterations = options.iter
infile = options.infile
outfile = options.outfile
verbose = options.verbose

# other constants
start_time = time.time() ## I always time my code ...

def genTS(arr):
    arr, source, bandWidth = trimDec(arr)

    # scramble azimuth data
    arr['ra'] = np.random.rand(len(arr)) * 2 * np.pi

    # calculate distance of each event from source
    distFromSource = np.sqrt((arr['ra'] - source['ra'])**2 + (arr['dec'] - source['dec'])**2)

    # return as likelihood
    return len([x for x in distFromSource if x < bandWidth])

def trimDec(arr):
    # define source
    source = {'name':'Milagro 1908',
              'sigma':np.radians(0.06),
              'ra':np.radians(287.05),
              'dec':np.radians(6.39)}

    # use 1 degree band
#    bandWidth = 3 * source['sigma']
    bandWidth = np.radians(1)

    # trim to dec band around source and return
    return (np.array([x for x in arr.T if np.abs(x['dec']-source['dec']) < bandWidth]),
            source,
            bandWidth)

def genTSD(arr, iterations):
    # return as a test statistic distribution
    return [genTS(arr) for _ in xrange(iterations)]

arr = np.load(infile)

data = genTSD(arr, iterations)

if verbose:
    print ('#### numpy file loaded {0} ...'.format(infile))
    print ('#### numpy file dump to {0} ...'.format(outfile))
    print ('####')

### dump it out as a numpy file
np.save(outfile, np.array([data, arr]))

if verbose:
    print ('#### ... it took {0} minuites'.format((time.time() - start_time)/60.))
    print ('#### DONE :D')
