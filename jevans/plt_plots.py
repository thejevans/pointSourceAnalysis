'''
Custom plotting functions using matplotlib
'''

import matplotlib.pyplot as plt

def hist2d (fig, ax, xs, ys, x_bins = 10, y_bins = 10, title = '', x_label = '', 
            y_label = '', show_counts = True):
    '''
    fig, ax, xs, ys, x_bins = 10, y_bins = 10, title = '', x_label = '', y_label = '', 
    show_counts = True
    
    fig:         pyplot figure
    ax:          pyplot axis
    xs:          data to be used for x axis
    ys:          data to be used for y axis
    x_bins:      number of bins for the x axis
    y_bins:      number of bins for the y axis
    title:       plot title
    x_label:     label for x axis
    y_label:     label for y axis
    show_counts: boolean value for whether or not to show the number of counts in each bins
    '''
    # Generate pyplot 2D hist
    
    h, xedges, yedges, image = ax.hist2d(xs, ys, [x_bins, y_bins])
    
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.grid(True)
    
    if show_counts:
        for i in range(len(yedges)-1):
            for j in range(len(xedges)-1):
                ax.text(xedges[j]+0.5,yedges[i]+0.5, hist[i,j], color="w", ha="center", 
                va="center", fontweight="bold")
    
    return fig, ax