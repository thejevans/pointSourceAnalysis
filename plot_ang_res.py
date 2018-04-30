'''
Plots angular resolution of either data or monte carlo
'''
from jevans.plt_plots import hist2d
from jevans.calculate import ang_res
import matplotlib.pyplot as plt
import numpy as np
import pickle as pkl
import argparse

# Parse arguments
parser = argparse.ArgumentParser(description='Plot angular resolution in a 2D histogram')
parser.add_argument('data', metavar='DATA', type=str,
                    help='numpy input file')
parser.add_argument('x_axis', metavar='X_INDEX', type=str, default='0'
                    help='index of x axis')
parser.add_argument('y_axis', metavar='Y_INDEX', type=str, default='1'
                    help='index of y axis')
parser.add_argument('--title', dest='title', type=str, default=''
                    help='title of plot')
parser.add_argument('--xlbl', dest='xlbl', type=str, default='Energy'
                    help='x axis label of plot')
parser.add_argument('--mc', dest='is_mc', action='store_const', const=True, default=False,
                    help='mark if DATA is a mote carlo file')

args = parser.parse_args()

# Get data
data = np.load(args.data)
if args.is_mc:
    temp = []
    temp[0] = ang_res(data)
    temp[1] = data[args.y_axis]
    data = temp
    x_axis = 0
    y_axis = 1
else:
    x_axis = args.x_axis
    y_axis = args.y_axis
    if x_axis.isdigit():
        x_axis = int(x_axis)
        y_axis = int(y_axis)

x_bins = 10
y_bins = 10

title   = args.title
x_label = args.xlbl
y_label = args.ylbl

# Create fig, ax
fig, ax = plt.subplots()

#plot
fig, ax = hist2d(fig, ax, data[x_axis], data[y_axis], x_bins = x_bins, y_bins = y_bins, 
                 title = title, x_label = x_label, y_label = y_label)

# Save Plot
plt.savefig(sys.argv[1])
