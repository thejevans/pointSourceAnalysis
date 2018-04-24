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

    bg_n = calculate.background_rate(source, bin_radians, bg, time_window) * time_window * calculate.bin_area(bin_radians)

    print ('#### bg done')

    mc = mc[calculate.signal_cut(source, bin_radians, mc)]

    print ('#### mc selection done')

    sig, sig_list = calculate.mc_weight(mc, index, time_window)

    print ('#### sig done')

    sig_sqrt_bg = sig / np.sqrt(bg_n)

    print ('#### bin {:.1f} done'.format(bin_diameter))
    print ('#### numpy file loaded {0} ...'.format(sys.argv[2]))
    print ('#### numpy file loaded {0} ...'.format(sys.argv[3]))
    print ('#### pickle file dump to {0} ...'.format(sys.argv[1]))
    print ('####')

    f = open(sys.argv[1], 'wb')
    pickle.dump((sig_sqrt_bg, bin_diameter, index, bg_n, sig, sig_list), f)
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

    for x in set(zip(*data)[2]):
        temp = ([],[],x,[],[])
        for y in data:
            if y[2] == x:
                temp[0].append(y[0])
                temp[1].append(y[1])
                temp[3].append(y[3])
                temp[4].append(y[4])
        temp = ([z/sum(temp[0]) for z in temp[0]], temp[1], temp[2], temp[3])
        munged_data.append(temp)

    munged_data.sort(key=operator.itemgetter(2))
    max_xs = []

    for x in munged_data[::-1]:
        plt.step(x[1], x[0], label = r'$E^{'+str(x[2])+r'}$')
        max_index = x[0].index(max(x[0]))
        max_xs.append(x[1][max_index])

    plt.grid(True)
    plt.xlabel(r'bin diameter $[^{\circ}]$')
    plt.ylabel(r'normalized $\frac{S}{\sqrt{B}}$')
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.legend(loc='best')

    ax = plt.gca()
    ax2 = ax.twiny()
    ax2.set_xticks(max_xs)
    ax2.set_xlim(ax.get_xlim())
    ax2.tick_params(axis='x', labelsize=8)
    ax2.xaxis.set_major_formatter(FormatStrFormatter('%g'))

    plt.savefig(''.join([sys.argv[1], '.pdf']))
    plt.close()
