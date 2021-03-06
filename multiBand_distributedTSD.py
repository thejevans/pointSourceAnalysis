#!/usr/bin/env python
from __future__ import print_function
from optparse import OptionParser
import numpy as np
import getBackground

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
parser.add_option("-s", "--steps", type = "int",
                  default = 10,
                  help = "number of steps")
parser.add_option("-v", "--verbose", action = "store_true",
                  default = False,
                  help = "print out if true")
(options, args) = parser.parse_args()

iterations = options.iter
steps      = options.steps
infile     = options.infile
outfile    = options.outfile
verbose    = options.verbose

# other constants
start_time = time.time() ## I always time my code ...

arr = np.load(infile)

start = np.radians(.5)
stop  = np.radians(5)
step  = (stop - start) / steps

data = np.empty(steps, dtype = [('bandWidth', np.float),('TSD', np.int, iterations)])

for i, band in enumerate(np.arange(start, stop, step)):
    data['bandWidth'][i] = band
    data['TSD'][i][:] = getBackground.genTSD(arr, bandWidth = band, iterations = iterations)

if verbose:
    print ('#### numpy file loaded {0} ...'.format(infile))
    print ('#### numpy file dump to {0} ...'.format(outfile))
    print ('####')

### dump it out as a numpy file
np.save(outfile, np.array([data, arr]))

if verbose:
    print ('#### ... it took {0} minuites'.format((time.time() - start_time)/60.))
    print ('#### DONE :D')
