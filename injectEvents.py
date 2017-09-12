import numpy as np
from numpy import random
import getBackground
import matplotlib.pyplot as plt

def genTS(arr,
          bandWidth = np.radians(1),
          pos_mu = None,
          pos_sigma = 1.0,
          rate_mu = None,
          rate_sigma = None,
          lam = None):

    # get rate of events from source
    if rate_mu is not None and rate_sigma is not None:
        rate = getRateGaussian(rate_mu, rate_sigma)
    elif lam is not None:
        rate = getRatePoisson(lam)
    else:
        return None

    # get background distribution
    backgroundTS, source = getBackground.scramble(arr, bandWidth)

    if pos_mu is None:
        pos_mu = [source['ra'], source['dec']]

    # return as likelihood
    return likelihood(backgroundTS, bandWidth, source, rate, pos_mu, pos_sigma)

def likelihood(backgroundTS, bandWidth, source, rate, pos_mu, pos_sigma):
    RAs, Decs = backgroundTS['ra'], backgroundTS['dec']

    # randomly remove number of background events equal to rate value
    for _ in xrange(rate):
        index = int(len(RAs) * random.rand())
        RAs = np.delete(RAs, index)
        Decs = np.delete(Decs, index)

    # generate each event based on position arguments, add to background
    for _ in xrange(rate):
        ra, dec = getPosition(pos_mu, pos_sigma)
        RAs = np.append(RAs, ra)
        Decs = np.append(Decs, dec)

    # calculate distance of each event from source
    distFromSource = np.sqrt((RAs - source['ra'])**2 + (Decs - source['dec'])**2)

    return len([x for x in distFromSource if x < bandWidth])

def genTSD(arr,
           iterations = 10000,
           bandWidth = np.radians(1),
           pos_mu = None,
           pos_sigma = 1.0,
           rate_mu = None,
           rate_sigma = None,
           lam = None):
    # return as a test statistic distribution
    args = arr, bandWidth, pos_mu, pos_sigma, rate_mu, rate_sigma, lam
    return [genTS(*args) for _ in xrange(iterations)]

def getRateGaussian(mu, sigma):
    # define injection rate distribution
    return np.random.normal(mu, sigma, 1)

def getRatePoisson(lam):
    # define injection rate distribution
    return np.random.poisson(lam)

def getPosition(mu, sigma):
    # define position distribution
    return np.random.multivariate_normal(mu, sigma * np.identity(2))

def plotTSD(TSD, arr, outfile, bandWidth = np.radians(1)):
    arr, source = getBackground.trimDec(arr, bandWidth)

    # plot formatting
    mainTitle = r'TSD of 10$^{{ {0:g} }}$ trials, {1:g} events/trial, '
    subTitle  = u'{2:4g}\xb0 around {3}'
    title     = '\n'.join([mainTitle,subTitle])
    fig, ax   = plt.subplots()

    # plot TSD
    hist = ax.hist(TSD, bins = max(TSD) - min(TSD), log = True, align = 'left', histtype='step')

    # compute p-values
    # ccdf = 1 - np.cumsum(hist[0]) * 1./np.sum(hist[0])

    # compute mean and sigma
    # mean, sigma = np.mean(TSD), np.std(TSD)

    # set x ticks
    # xticks = range(int(mean - 5 * sigma),int(mean + 5 * sigma), int(sigma))
    # ax.set_xticks(xticks)

    # more plot formatting
    # ax.set_xlim(max(0, mean - 5 * sigma), mean + 5 * sigma)
    ax.set_ylim(1, 10**(int(np.log10(max(hist[0]))) + 1))
    plt.title(title.format(np.log10(len(TSD)), len(arr), np.degrees(bandWidth), source['name']))
    plt.xlabel('Number of Events in Bin')
    plt.ylabel('Counts', color = 'b')
    # plt.axvline(x = mean, linestyle = '--')
    # ax2 = ax.twinx()
    # ax3 = ax.twiny()

    # plot p-values
    # ax2.plot(hist[1][:-1], ccdf, 'r-')

    # shade 3 sigma interval
    # plt.axvspan(mean - 3 * sigma, mean + 3 * sigma, facecolor='0.2', alpha=0.5)

    # even more plot formatting
    # ax2.set_ylabel('p-value', color = 'r')
    # ax2.set_xlim(max(0, mean - 5 * sigma), mean + 5 * sigma)
    # ticks = [(mean - 3 * sigma, r'3$\sigma$'),
    #               (mean - sigma, r'$\sigma$'),
    #               (mean, r'$\mu$'),
    #               (mean + sigma, r'$\sigma$'),
    #               (mean + 3 * sigma, r'3$\sigma$'),
    #               (mean + 5 * sigma, r'5$\sigma$')]
    # ax3.set_xticks([x[0] for x in ticks])
    # ax3.set_xticklabels([x[1] for x in ticks])
    # ax3.set_xlim(max(0, mean - 5 * sigma), mean + 5 * sigma)

    # save and close plot
    fig.savefig(outfile)
    plt.close()

    return hist[1][:-1]
