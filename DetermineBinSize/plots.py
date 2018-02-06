import pandas as pd
import seaborn as sns
import likelihood
from itertools import product

def RateVsBin(mc, rates, bins, rateType = 'value', outfile = 'out.csv', **kwargs):
    likelihoods = {}

    for rate, binDiameter in product(rates, bins):
        likelihoods.update({(rate, binDiameter):likelihood.getLikelihood(*{
        'value':    (mc, rate_value = rate, binDiameter = binDiameter, **kwargs),
        'poisson':  (mc, lam = rate, binDiameter = binDiameter, **kwargs),
        'gaussian': (mc, rate_mu = rate['mu'], rate_sigma = rate['sigma'], binDiameter = binDiameter, **kwargs)
        }[rateType])})

    output(likelihoods,outfile)

def RateVsIndex(mc, rates, spectralIndicies, rateType = 'value', outfile = 'out.csv', **kwargs):
    likelihoods = {}

    for rate, spectralIndex in product(rates, spectralIndicies):
        likelihoods.update({(rate, spectralIndex):likelihood.getLikelihood(*{
        'value':    (mc, rate_value = rate, spectralIndex = spectralIndex, **kwargs),
        'poisson':  (mc, lam = rate, spectralIndex = spectralIndex, **kwargs),
        'gaussian': (mc, rate_mu = rate['mu'], rate_sigma = rate['sigma'], spectralIndex = spectralIndex, **kwargs)
        }[rateType])})

    output(likelihoods,outfile)

def output(likelihoods, outfile):
    if outfile[outfile.rfind('.')+1:] == 'csv':
        df = munge(likelihoods)
        df.to_csv(outfile, sep='\t')
    else:
        heatmap = sns.heatmap(munge(likelihoods), annot=True)
        fig = heatmap.get_figure()
        fig.savefig(outfile)

def munge(likelihoods):
    s  = pd.Series(likelihoods, index=pd.MultiIndex.from_tuples(likelihoods))
    df = s.unstack()
    df.combine_first(df.T).fillna(0)
