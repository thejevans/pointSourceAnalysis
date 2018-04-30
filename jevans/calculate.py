import numpy as np

def background_rate(source, band_width, arr, time_window):
    # solid angle area
    area = 360**2 * (np.cos(source['ra'] + band_width / 2) + np.cos(np.cos(source['ra'] 
                     - band_width / 2))) / (2 * np.pi)
    # get list of events in band
    events = [x for x in arr.T if np.abs(x['dec']-source['dec']) < (band_width / 2)]
    return len(events) / (area * time_window)

def signal_cut(source, band_width, mc):
    in_band = [delta_angle(x['ra'], 0, source['ra'],0) < band_width / 2 for x in mc]
    in_bin  = [delta_angle(x['zenith'], x['azimuth'], x['trueZenith'], x['trueAzimuth']) 
               < band_width / 2 for x in mc]
    product = [a*b for a,b in zip(in_band,in_bin)]
    return np.array(product, dtype = bool)

def mc_weight(mc, spectral_index, time_window):
    reweight = lambda x: 1e-18 * x['ow'] * np.power(x['trueE']/100e3, spectral_index) * time_window
    weights = [reweight(x) for x in mc]
    return sum(weights), weights

def delta_angle(ra1, dec1, ra2, dec2):
    # theta is angular distance in radians
    cos_theta = np.sin(dec1) * np.sin(dec2) + np.cos(dec1) * np.cos(dec2) * np.cos(ra1 - ra2)
    return np.abs(np.arccos(cos_theta))

def ang_res(mc):
    delta_angles = [delta_angle(x['zenith'], x['azimuth'], x['trueZenith'], 
                                x['trueAzimuth']) for x in mc]
    mean = np.mean(delta_angles)
    minimum = min(delta_angles)
    maximum = max(delta_angles)
    return delta_angles, mean, minimum, maximum

def bin_area(band_width):
    # solid angle area
    return 360**2 * (1 - np.cos(band_width / 2)) / (2 * np.pi)
