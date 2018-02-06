import pandas as pd
import seaborn as sns
import likelihood
from itertools import product

def RateVsBin(mc, rates, bins, rateType = 'value', outfile = 'out.csv', **kwargs):
    likelihoods = {}
    kwargs2 = {}

    for rate, binDiameter in product(rates, bins):
        kwargs2 = {'value':    {'rate_value': rate, 'binDiameter': binDiameter},
                   'poisson':  {'lam': rate, 'binDiameter': binDiameter},
                   #'gaussian': {'rate_mu': rate['mu'], 'rate_sigma': rate['sigma'], 'binDiameter': binDiameter}
        }[rateType]
        kwargs2.update(kwargs)
        likelihoods.update({(rate, binDiameter):likelihood.getLikelihood(mc, **kwargs2)})

    output(likelihoods,outfile)

def RateVsIndex(mc, rates, spectralIndicies, rateType = 'value', outfile = 'out.csv', **kwargs):
    likelihoods = {}
    kwargs2 = {}

    for rate, spectralIndex in product(rates, spectralIndicies):
        kwargs2 = {'value':    {'rate_value': rate, 'spectralIndex': spectralIndex},
                   'poisson':  {'lam': rate, 'spectralIndex': spectralIndex},
                   #'gaussian': {'rate_mu': rate['mu'], 'rate_sigma': rate['sigma'], 'spectralIndex': spectralIndex}
        }[rateType]
        kwargs2.update(kwargs)
        likelihoods.update({(rate, spectralIndex):likelihood.getLikelihood(mc, **kwargs2)})

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
