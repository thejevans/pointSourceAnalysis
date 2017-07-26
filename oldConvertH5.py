import tables
import numpy as np
from utils.coords import local2eq
print("IC86")

deg5 = np.radians(5.)

pull = lambda X: (79. - 86.7 * X + 38.45 * X**2 - 8.673 * X**3
                  + 1.056 * X**4 - 0.0658 * X**5 + 0.00165 * X**6)

hdf = tables.openFile("./PrunedDataUpgoing.hd5")

f = hdf.root

data = f.SplineMPEParaboloidFitParams.cols
pbf_status = ((data.err1[:] >= 0)&(data.err2[:] >= 0))
paraboloid_sigma = np.sqrt(data.err1[:]**2 + data.err2[:]**2) / np.sqrt(2)

print("\t\t{0:7.2%} Paraboloid OK".format(
    np.sum(pbf_status, dtype=np.float) / len(pbf_status)))

pbf_status2 = data.status[:] >= 0
print("\t\t{0:7.2%} Paraboloid not complete fail".format(
    np.sum(pbf_status2, dtype=np.float) / len(pbf_status2)))

arr = np.empty((np.sum(pbf_status), ), dtype=[("run", np.int),
                                              ("event", np.int),
                                              ("ra", np.float),
                                              ("dec", np.float),
                                              ("azimuth",np.float),
                                              ("zenith",np.float),
                                              ("logE", np.float),
                                              ("sigma", np.float),
                                              ("time", np.float)])

arr["run"] = f.I3EventHeader.cols.Run[:][pbf_status]
arr["event"] = f.I3EventHeader.cols.Event[:][pbf_status]

data = f.SplineMPE.cols
zen = data.zenith[:][pbf_status]
phi = data.azimuth[:][pbf_status]
arr["azimuth"] = data.azimuth[:][pbf_status]
arr["zenith"] = data.zenith[:][pbf_status]
data = f
arr["time"] = data.timeMJD.cols.value[:][pbf_status]
arr["ra"], arr["dec"] = local2eq(zen, phi, arr["time"])

data = f.SplineMPEMuEXDifferential.cols
arr["logE"] = np.log10(data.energy[:][pbf_status])
arr["sigma"] = paraboloid_sigma[:][pbf_status] * pull(arr["logE"])

sigma_status = arr["sigma"] < deg5
print("\t5deg threshold: {0:7.2%}".format(
    np.sum(sigma_status, dtype=np.float) / len(sigma_status)))

arr = arr[sigma_status]

print "Paraboloid:", np.degrees(np.percentile(arr["sigma"],
                                                [0., 50., 90., 95., 100.]))

hdf.close()

print("\t{0:6d} events".format(len(arr)))
np.save("IC86_exp.npy", arr)
