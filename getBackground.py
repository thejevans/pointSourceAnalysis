import numpy as np

def genTS(arr):
    # define Milagro 1908
    mgro1908 = {'sigma':np.radians(0.06), 'ra':np.radians(287.05), 'dec':np.radians(6.39)}

    # trim to 3-sigma dec band around Milagro 1908
    arr = np.array([x for x in arr.T if np.abs(x['dec']-mgro1908['dec']) < 3 * mgro1908['sigma']])

    # scramble azimuth data
    arr['ra'] = np.random.rand(len(arr)) * 2 * np.pi

    # calculate distance of each event from Milagro 1908
    distFromSource = np.sqrt((arr['ra'] - mgro1908['ra'])**2 + (arr['dec'] - mgro1908['dec'])**2)

    # return as background test statistic and likelihood
    return arr, len([x for x in distFromSource if x < 3 * mgro1908['sigma']])
