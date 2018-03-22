import numpy as np
import calculate
import sys
import matplotlib.pyplot as plt
import pickle

if sys.argv[1][-3:] == 'npy':
    arr    = np.load(sys.argv[1])
    bins   = np.radians(np.arange(0.1, 5, .01))
    source = {'name':'Milagro 1908',
              'sigma':np.radians(0.06),
              'ra':np.radians(287.05),
              'dec':np.radians(6.39)}
    time   = 365 * 24 * 60 * 60 * int(sys.argv[3])
    bgs    = [calculate.background_rate(source, x, arr, time) for x in bins]

    f = open(''.join(['./', sys.argv[2], '.pkl']), 'wb')
    pickle.dump((bins, bgs), f)
    f.close()

elif sys.argv[1][-3:] == 'pkl':
    f         = open(sys.argv[1], 'rb')
    bins, bgs = pickle.load(f)
    f.close()

plt.plot(np.degrees(bins), bgs)
plt.xlabel('Bin Diameter in degrees')
plt.ylabel('Number of expected background neutrinos per square degree per year')
plt.savefig(''.join(['./', sys.argv[2], '.pdf']))
