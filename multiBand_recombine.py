#!/usr/bin/env python

'''

'''

from __future__ import print_function
from optparse import OptionParser
import numpy as np
from glob import glob
import getBackground
import matplotlib.pyplot as plt

# Command parsing
usage = '%prog [options] --indir <input directory> --outdir <output directory>'
parser = OptionParser(usage = usage, description=__doc__)
parser.add_option('-i', '--indir', type = 'string',
                  default = '/data/i3store0/users/jevans96/point_source_analysis/distributed_outputs/data/',
                  help = 'Directory containing numpy files')
parser.add_option('-o', '--outdir', type = 'string',
                  default = '/data/i3store0/users/jevans96/point_source_analysis/charts/',
                  help = 'Directory to output histogram')
parser.add_option("-t", "--iter", type = "int",
                  default = 10,
                  help = "number of iterations")
parser.add_option("-s", "--steps", type = "int",
                  default = 10,
                  help = "number of steps")
(options, args) = parser.parse_args()

iterations = options.iter
steps      = options.steps
inDir      = options.indir
outDir     = options.outdir

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
data = np.empty(steps, dtype = [('bandWidth', np.float), ('TSD', np.int, iterations)])
data['bandWidth'] = arr[0]['bandWidth']

for i, filename in enumerate(filenames):
    for j, TSD in enumerate(np.load(filename)[0]['TSD']):
        data['TSD'][j][i * iterations / len(filenames):(i + 1) * iterations / len(filenames)] = TSD

# Set output file name based on input file name
outFilename = ''.join([outDir, 'multiBand_TSD_{0}_Trials'.format(len(data['TSD'][0]))])
np.save('.'.join([outFilename,'npy']), data)

# plots
hist = np.empty(0, dtype = [('bandWidth', np.float), ('count', np.int), ('ccdf', np.float)])
mean = sigma = np.empty(len(data['bandWidth']))
for i, band in enumerate(arr[0]['bandWidth']):
    counts, ccdf, mean[i], sigma[i] = getBackground.plotTSD(data['TSD'][i], arr[1],
                                         '.'.join([outFilename, 'band_{0}'.format(i), 'png']),
                                         bandWidth = band)
    old_len = len(hist)
    hist.resize(old_len + len(counts))
    hist['bandWidth'][old_len:len(hist)] = np.ones(len(counts)) * np.degrees(band)
    hist['count'][old_len:len(hist)] = counts
    hist['ccdf'][old_len:len(hist)] = ccdf

with open('./table.csv', 'w') as fp:
    fp.write('\n'.join([','.join(['','','Number of Events']),
                        ','.join(['Bin Size','Mean','2 Sigma','3 Sigma','4 Sigma','5 Sigma']),
                        '']))
    for i in xrange(len(data['bandWidth'])):
        fp.write(','.join([str(np.degrees(data['bandWidth'][i])),
                           str(mean[i]),
                           str(mean[i] + 2*sigma[i]),
                           str(mean[i] + 3*sigma[i]),
                           str(mean[i] + 4*sigma[i]),
                           str(mean[i] + 5*sigma[i])]) + '\n')


minBand = max(hist['bandWidth'])
maxBand = 0
maxCount = 0

for i in xrange(min(hist['count']), max(hist['count'])):
    temp = np.array([x for x in hist.T if x['count'] == i])
    if not (min(temp['bandWidth']) <= 1 <= max(temp['bandWidth'])):
        continue
    if min(temp['bandWidth']) < minBand:
        minBand = min(temp['bandWidth'])
    if max(temp['bandWidth']) > maxBand:
        maxBand = max(temp['bandWidth'])
    maxCount = i
    fig, ax = plt.subplots()
    ax.plot(temp['bandWidth'], temp['ccdf'])
    plt.xlabel('Band Width')
    plt.ylabel('p-value')
    plt.axvline(x = 1, linestyle = '--')
    plt.title('count = {0}'.format(i))
    fig.savefig('_'.join([outFilename, 'p-values_{0}.png'.format(i)]))
    plt.close()


fig, ax = plt.subplots()
im = ax.scatter(hist['bandWidth'], hist['count'], c = hist['ccdf'], marker = '.', linewidth = 0)

clb = fig.colorbar(im, ax=ax)
clb.set_label('p-value')

plt.axis([minBand, maxBand, min(hist['count']), maxCount])
plt.xlabel('Declination band width')
plt.ylabel('Number of events within 1 band width circle of Milagro 1908')

fig.savefig('_'.join([outFilename, 'p-values_all.png']))
plt.close()
