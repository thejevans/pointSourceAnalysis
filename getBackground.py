import numpy as np
import matplotlib.pyplot as plt

def genTS(arr, bandWidth = np.radians(1)):
    arr, source = trimDec(arr, bandWidth)

    # scramble azimuth data
    arr['ra'] = np.random.rand(len(arr)) * 2 * np.pi

    # calculate distance of each event from source
    distFromSource = np.sqrt((arr['ra'] - source['ra'])**2 + (arr['dec'] - source['dec'])**2)

    # return as likelihood
    return len([x for x in distFromSource if x < bandWidth])

def trimDec(arr, bandWidth = np.radians(1)):
    # define source
    source = {'name':'Milagro 1908',
              'sigma':np.radians(0.06),
              'ra':np.radians(287.05),
              'dec':np.radians(6.39)}

    # use 1 degree band
#    bandWidth = 3 * source['sigma']

    # trim to dec band around source and return
    return (np.array([x for x in arr.T if np.abs(x['dec']-source['dec']) < bandWidth]),
            source)

def genTSD(arr, iterations = 10000, bandWidth = np.radians(1)):
    # return as a test statistic distribution
    return [genTS(arr, bandWidth) for _ in xrange(iterations)]

def plotTSD(TSD, arr, outfile, bandWidth = np.radians(1)):
    arr, source = trimDec(arr, bandWidth)

    # plot formatting
    mainTitle = r'Test statistic distribution of 10$^{{ {0:d} }}$ trials, {1:d} events per trial'
    subTitle  = u'{2:4g}\xb0 around {3}'
    title     = '\n'.join([mainTitle,subTitle])
    fig, ax   = plt.subplots()

    # plot TSD
    hist = ax.hist(TSD, bins = max(TSD) - min(TSD), log = True, align = 'left', histtype='step')

    # compute p-values
    ccdf = 1 - np.cumsum(hist[0]) * 1./np.sum(hist[0])

    # more plot formatting
    ax.set_xticks(range(int(min(TSD)),int(max(TSD)), int((max(TSD) - min(TSD))/10)))
    ax.set_xlim(min(TSD) - .5, max(TSD) - .5)
    ax.set_ylim(1, 10**(int(np.log10(max(hist[0]))) + 1))
    plt.title(title.format(np.log10(len(TSD)), len(arr), np.degrees(bandWidth), source['name']))
    plt.xlabel('Background Likelihood')
    plt.ylabel(r'log$_{10}$ Frequency', color = 'b')
    ax2 = ax.twinx()

    # plot p-values
    ax2.plot(hist[1][:-1], ccdf, 'r-')

    # shade .05 to .95 interval
    #plt.axvspan(hist[1][np.argmin((0.95-ccdf)**2)],
    #            hist[1][np.argmin((0.05-ccdf)**2)],
    #            facecolor='0.2',
    #            alpha=0.5)

    # even more plot formatting
    ax2.set_xlim(min(TSD) - .5, max(TSD) - .5)
    ax2.set_ylabel('p-value', color = 'r')

    # save plot
    fig.savefig(outfile)
