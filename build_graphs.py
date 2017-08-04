import numpy as np
import matplotlib.pyplot as plt

def graph(inFile, outDir):
    # load npy file
    arr = np.load(inFile)

    # remove points with negative angular error
    old_len      = float(len(arr))
    arr          = np.extract(arr['ang_err']>0, arr)
    percent_loss = 100 * (old_len / len(arr) - 1)
    print(''.format())

    # graph...something
    with plt.xkcd():
        fig, ax = plt.subplots()
        im      = ax.scatter(arr['logE'],
                             arr['ang_err'],
                             c=arr['zenith']/np.pi,
                             marker='.',
                             linewidth=0.0)

        clb = fig.colorbar(im, ax=ax)

        plt.axis([0, 7, min(arr['ang_err']), max(arr['ang_err'])])

        plt.xlabel('log_10 E')
        plt.ylabel('angular error')
        clb.set_label('zenith / pi')

        fig.savefig('./foo.png')
    # save graph

    # repeat if necessary
