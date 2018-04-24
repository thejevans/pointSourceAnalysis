#!/usr/bin/env python
from __future__ import print_function
import numpy as np
import calculate
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import pickle
import time, socket
from glob import glob
import operator

if sys.argv[2][-3:] == 'npy': #distributed computing case
    print ('########################################################################################')
    print ('#### This job is running on {0}'.format(socket.gethostname()))
    print ('########################################################################################')
    print (' ')

    start_time   = time.time()
    bin_diameter = float(sys.argv[4])
    bin_radians  = np.radians(bin_diameter)

    index  = -1 * float(sys.argv[5])
    mc     = np.load(sys.argv[2])
    bg     = np.load(sys.argv[3])
    time_window = 365 * 24 * 60 * 60
    source = {'name':'Milagro 1908',
              'sigma':np.radians(0.06),
              'ra':np.radians(287.05),
              'dec':np.radians(6.39)}

    mc = mc[calculate.signal_cut(source, bin_radians, mc)]

    print ('#### mc selection done')

    mean, minimum, maximum = calculate.ang_res(mc)

    print ('#### ang res done')
    print ('#### bin {:.1f} done'.format(bin_diameter))
    print ('#### numpy file loaded {0} ...'.format(sys.argv[2]))
    print ('#### numpy file loaded {0} ...'.format(sys.argv[3]))
    print ('#### pickle file dump to {0} ...'.format(sys.argv[1]))
    print ('####')

    f = open(sys.argv[1], 'wb')
    pickle.dump((bin_diameter, index, mean, minimum, maximum), f)
    f.close()

    end_time = (time.time() - start_time)/60.
    print ('#### ... it took {0} minutes'.format(end_time))
    print ('#### DONE :D')

elif sys.argv[2][-1:] == '/': #recombine case
    filenames = sorted(glob(''.join([sys.argv[2], '*.pkl'])))
    data = []

    for x in filenames:
        f = open(x, 'rb')
        data.append(pickle.load(f))
        f.close()

    f = open(sys.argv[1], 'wb')
    pickle.dump(data, f)
    f.close()

elif sys.argv[2][-3:] == 'pkl': #plot case
    f    = open(sys.argv[2], 'rb')
    data = pickle.load(f)
    f.close()

    munged_data = []

    for x in set(zip(*data)[1]):
        temp = ([],x,[],[],[])
        for y in data:
            if y[1] == x:
                temp[0].append(y[0])
                temp[2].append(np.degrees(y[2]))
                temp[3].append(np.degrees(y[3]))
                temp[4].append(np.degrees(y[4]))
        munged_data.append(temp)

    munged_data.sort(key=operator.itemgetter(1))

    #mean
    max_xs = []

    x = munged_data[0]
    plt.step(x[0], x[2])
    max_index = x[2].index(max(x[2]))
    max_xs.append(x[0][max_index])

    plt.grid(True)
    plt.xlabel(r'bin diameter $[^{\circ}]$')
    plt.ylabel(r'mean delta angle $[^{\circ}]$')
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)

    ax = plt.gca()
    ax2 = ax.twiny()
    ax2.set_xticks(max_xs)
    ax2.set_xlim(ax.get_xlim())
    ax2.tick_params(axis='x', labelsize=8)
    ax2.xaxis.set_major_formatter(FormatStrFormatter('%g'))

    plt.savefig(''.join([sys.argv[1], '_mean.pdf']))
    plt.close()

    #max
    max_xs = []

    x = munged_data[0]
    plt.step(x[0], x[4])
    max_index = x[4].index(max(x[4]))
    max_xs.append(x[0][max_index])

    plt.grid(True)
    plt.xlabel(r'bin diameter $[^{\circ}]$')
    plt.ylabel(r'max delta angle $[^{\circ}]$')
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)

    ax = plt.gca()
    ax2 = ax.twiny()
    ax2.set_xticks(max_xs)
    ax2.set_xlim(ax.get_xlim())
    ax2.tick_params(axis='x', labelsize=8)
    ax2.xaxis.set_major_formatter(FormatStrFormatter('%g'))

    plt.savefig(''.join([sys.argv[1], '_max.pdf']))
    plt.close()

    #min
    max_xs = []

    x = munged_data[0]
    plt.step(x[0], x[3])
    max_index = x[3].index(max(x[3]))
    max_xs.append(x[0][max_index])

    plt.grid(True)
    plt.xlabel(r'bin diameter $[^{\circ}]$')
    plt.ylabel(r'min delta angle $[^{\circ}]$')
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)

    ax = plt.gca()
    ax2 = ax.twiny()
    ax2.set_xticks(max_xs)
    ax2.set_xlim(ax.get_xlim())
    ax2.tick_params(axis='x', labelsize=8)
    ax2.xaxis.set_major_formatter(FormatStrFormatter('%g'))

    plt.savefig(''.join([sys.argv[1], '_min.pdf']))
    plt.close()
