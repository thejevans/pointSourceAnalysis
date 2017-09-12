import numpy as np
import matplotlib.pyplot as plt

def genTS(arr, bandWidth = np.radians(1)):
    arr, source = scramble(arr, bandWidth)

    # calculate distance of each event from source
    distFromSource = np.sqrt((arr['ra'] - source['ra'])**2 + (arr['dec'] - source['dec'])**2)

    # return as likelihood
    return len([x for x in distFromSource if x < bandWidth]), arr

def scramble(arr, bandWidth):
    arr, source = trimDec(arr, bandWidth)

    # scramble azimuth data
    arr['ra'] = np.random.rand(len(arr)) * 2 * np.pi

    return arr, source

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
    mainTitle = r'TSD of 10$^{{ {0:g} }}$ trials, {1:g} events/trial, '
    subTitle  = u'{2:4g}\xb0 around {3}'
    title     = ''.join([mainTitle,subTitle,'\n'])
    fig, ax   = plt.subplots()

    # plot TSD
    hist = ax.hist(TSD, bins = max(TSD) - min(TSD), log = True, align = 'left', histtype='step')

    # compute p-values
    ccdf = 1 - np.cumsum(hist[0]) * 1./np.sum(hist[0])

    # compute mean and sigma
    mean, sigma = np.mean(TSD), np.std(TSD)

    # set x ticks
    xticks = range(int(mean - 5 * sigma),int(mean + 5 * sigma), int(sigma))
    ax.set_xticks(xticks)

    # more plot formatting
    ax.set_xlim(max(0, mean - 5 * sigma), mean + 5 * sigma)
    ax.set_ylim(1, 10**(int(np.log10(max(hist[0]))) + 1))
    plt.title(title.format(np.log10(len(TSD)), len(arr), np.degrees(bandWidth), source['name']))
    plt.xlabel('Background Likelihood')
    plt.ylabel(r'log$_{10}$ Frequency', color = 'b')
    plt.axvline(x = mean, linestyle = '--')
    ax2 = ax.twinx()
    ax3 = ax.twiny()

    # plot p-values
    ax2.plot(hist[1][:-1], ccdf, 'r-')

    # shade 3 sigma interval
    plt.axvspan(mean - 3 * sigma, mean + 3 * sigma, facecolor='0.2', alpha=0.5)

    # even more plot formatting
    ax2.set_ylabel('p-value', color = 'r')
    ax2.set_xlim(max(0, mean - 5 * sigma), mean + 5 * sigma)
    ticks = [(mean - 3 * sigma, r'3$\sigma$'),
                  (mean - sigma, r'$\sigma$'),
                  (mean, r'$\mu$'),
                  (mean + sigma, r'$\sigma$'),
                  (mean + 3 * sigma, r'3$\sigma$'),
                  (mean + 5 * sigma, r'5$\sigma$')]
    ax3.set_xticks([x[0] for x in ticks])
    ax3.set_xticklabels([x[1] for x in ticks])
    ax3.set_xlim(max(0, mean - 5 * sigma), mean + 5 * sigma)

    # save and close plot
    fig.savefig(outfile)
    plt.close()

    return hist[1][:-1], ccdf, mean, sigma
