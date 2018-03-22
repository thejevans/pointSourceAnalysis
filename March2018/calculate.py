import numpy as np

def background_rate(source, band_width, arr, time_window):
    # solid angle area
    area = 360**2 * (np.cos(source['ra'] + band_width / 2) + np.cos(np.cos(source['ra'] - band_width / 2))) / (2 * np.pi)
    # get list of events in band
    events = [x for x in arr.T if np.abs(x['dec']-source['dec']) < (band_width / 2)]

    return len(events) / (area * time_window)

def signal_probability(source, spectral_index, lam, mc, time_window):
    sample   = lam #np.random.poisson(lam)
    reweight = lambda x: 1e-18 * x['ow'] * np.power(x['trueE']/100e3, spectral_index) * time_window
    # list of probabilities in time window
    w   = [reweight(x) for x in mc]
    arr = np.array([x for i,x in enumerate(mc) if w[i] > sample], dtype = mc.dtype)
    w   = [x for x in w if x > sample]
    # returns probability of seeing (lam) signal events in (time_window) seconds at (spectral_index)
    return np.sum(w), w, arr

def delta_angle((ra1, dec1), (ra2, dec2)):
    # theta is angular distance in radians
    cos_theta = np.sin(dec1) * np.sin(dec2) + np.cos(dec1) * np.cos(dec2) * np.sin(ra1 - ra2)
    return np.abs(np.arccos(cos_theta))

def bin_area(band_width):
    # solid angle area
    return 360**2 * (1 - np.cos(band_width / 2)) / (2 * np.pi)
