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
    index  = -2
    lam    = np.arange(1e-4,2.5e-4, 2e-6)
    reweight = lambda x: 1e-18 * x['ow'] * np.power(x['trueE']/100e3, index) * time
    # list of probabilities in time window
    w   = [reweight(x) for x in arr]
    sig    = [calculate.signal_probability(source, index, x, arr, time, w) for x in lam]

    f = open(''.join(['./', sys.argv[2], '.pkl']), 'wb')
    pickle.dump((lam, sig), f)
    f.close()

elif sys.argv[1][-3:] == 'pkl':
    f         = open(sys.argv[1], 'rb')
    lam, sig = pickle.load(f)
    lam = np.array(range(0,5))
    f.close()
print [x[0] for x in sig]

recon_minus_true = [calculate.delta_angle((x['ra'],x['dec']),(x['trueRa'],x['trueDec'])) for x in [x[2] for x in sig]]

w_bins = [[x for i,x in enumerate(sig[1]) if recon_minus_true[i] < y] for y in bins]
arr_bins = [np.array([x for i,x in enumerate(sig[2]) if recon_minus_true[i] < y], dtype = x.dtype) for y in bins]

sum_w_bins = [sum(x) for x in w_bins]

print(sum_w_bins)

# plt.plot(lam, sig)
# plt.xlabel('Bin Diameter in degrees')
# plt.ylabel('Number of expected signal neutrinos per square degree per year')
# plt.savefig(''.join(['./', sys.argv[2], '.pdf']))
