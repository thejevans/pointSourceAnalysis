import numpy as np
from numpy import random

source = {'name':'Milagro 1908',
          'sigma':np.radians(0.06),
          'ra':np.radians(287.05),
          'dec':np.radians(6.39)}

def getBackground(mc, timeWindow, spectralIndex, binDiameter):
    arr = inBin(mc, binDiameter)
    return np.sum(1e-18 * mc['ow'] * np.power(mc['trueE']/100e3, spectralIndex)) * timeWindow

def getSignal(binDiameter, mu, sigma, rate):
    data = np.empty(len(rate), dtype=[('ra', np.float), ('dec', np.float)])

    for i in xrange(rate):
        data[i]['ra'], data[i]['dec'] = np.random.multivariate_normal(mu, sigma * np.identity(2))

    return len(inBin(data, binDiameter))

def inBin(arr, binDiameter):
    distFromSource = lambda x: np.sqrt((x['ra'] - source['ra'])**2 + (x['dec'] - source['dec'])**2)
    return np.array([x for x in arr.T if distFromSource(x) < binDiameter])

def getLikelihood(mc,
                  spectralIndex = -2,
                  timeWindow    = 365*24*60*60,
                  binDiameter   = np.radians(1),
                  signal        = None,
                  pos_mu        = [source['ra'], source['dec']],
                  pos_sigma     = source['sigma'],
                  rate_mu       = None,
                  rate_sigma    = None,
                  rate_value    = None,
                  lam           = None):

    if rate_mu is not None and rate_sigma is not None:
        rate  = np.random.normal(rate_mu, rate_sigma, 1)
        sigma = np.sqrt(rate_sigma**2 + pos_sigma**2)
    elif lam is not None:
        rate  = np.random.poisson(lam)
        sigma = np.sqrt(lam + pos_sigma**2)
    elif rate_value is not None:
        rate  = rate_value
        sigma = pos_sigma
    else:
        return None

    if signal is None:
        signal = getSignal(binDiameter, pos_mu, pos_sigma, rate)

    theory = getBackground(mc, timeWindow, spectralIndex, binDiameter)

    return (signal - theory)**2/sigma**2
