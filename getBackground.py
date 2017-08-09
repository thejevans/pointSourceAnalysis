import numpy as np
import matplotlib.pyplot as plt

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

def plotTSD(TSD, arr, outfile):
    arr, source, bandWidth = trimDec(arr)
    # fig, ax = plt.subplots()
    # ax.hist(TSD, bins = max(TSD) - min(TSD), log = True, align = 'left')
    # ax.set_xticks(range(int(min(TSD)),int(max(TSD)), int((max(TSD) - min(TSD))/10)))
    # ax.set_xlim(min(TSD) - .5, max(TSD) - .5)
    # title = '\n'.join(['Test statistic distribution of {0:d} trials, {1:d} events per trial',
    #                   '{2:.2f} degree(s) around {3}'])
    # plt.title(title.format(len(TSD), len(arr), np.degrees(bandWidth), source['name']))
    # plt.xlabel('Background Likelihood')
    # plt.ylabel('log_10 Frequency')

    fig, ax = plt.subplots()
    ccdf = 1 - np.cumsum(TSD)/np.sum(TSD)
    ax.plot(ccdf)
    ax.set_xticks(range(int(min(ccdf)),int(max(ccdf)), int((max(ccdf) - min(ccdf))/10)))
    ax.set_xlim(min(ccdf) - .5, max(ccdf) - .5)
    ax.set_ylim(0,1)
    title = '\n'.join(['Test statistic distribution of {0:d} trials, {1:d} events per trial',
                      '{2:.2f} degree(s) around {3}'])
    plt.title(title.format(len(TSD), len(arr), np.degrees(bandWidth), source['name']))
    plt.xlabel('Background Likelihood')
    plt.ylabel('p-value')

    fig.savefig(outfile)
