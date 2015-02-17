#!/usr/bin/python

# last modified: 2015-02-11
# author:        tc

import sys
import os
import math
import numpy
from matplotlib import pyplot as plt

if len(sys.argv) != 2:
    sys.exit("GIVE ME INPUT IN THE FORM: NAME OF OBSERVABLE DATA FILE IN GRID DATA")

def err_independent(obs):
    """
    Error on the average of a set of independent samples.
    """
    if type(obs) is list:
        obs = numpy.array(obs)
    variance = numpy.mean(obs ** 2) - numpy.mean(obs) ** 2
    return math.sqrt(variance / float(len(obs)))

def bunching_v2(obs, base, namevar, datafile, plotname, DoPlot=True):
    """
    Binning procedure for a series of (correlated) samples.
    Input:
      obs      : array of samples
      base     : bin widths are taken to be 1, base, base^2, base^3..
                 (provided there are at least 32 points per bin, on average)
      namevar  : name of the variable
      datafile : output file for error analysis
      plotname : plot file for error analysis
      DoPlot   : whether to draw the plot or not 
    Output:
      binwidths : list of bin widths considered
      errors    : apparent error for the bin widths considered
      obs_av    : average of obs
        
    """
    # define bin widths, and keep them only if (average occupation) > 32
    binwidths = [base ** k for k in xrange(40)]
    binwidths = [width for width in binwidths if 32 * width < len(obs)]
    n_binwidths = len(binwidths)
    if n_binwidths < 2:
        sys.exit('ERROR: not enough data. Exit.')
    # perform binning
    old_list = []
    new_list = [i for i in obs]
    factors = [1] + [binwidths[i + 1] / binwidths[i] for i in xrange(n_binwidths - 1)]
    errors = []
    for l in xrange(n_binwidths):
       # one binning step
       factor = factors[l]
       old_list = new_list[:]
       size = len(old_list)
       new_list = []
       while size > factor:
          new_list.append(sum(old_list.pop() for i in xrange(factor)) / float(factor))
          size -= factor
       errors.append(err_independent(new_list))
    # write results
    f = open(datafile, "w")
    f.write('nsteps:         %i\n' % len(obs))
    f.write('bin-width base: %i\n' % base)
    f.write('min(binwidths): %i\n' % binwidths[0])
    f.write('max(binwidths): %i\n' % binwidths[-1])
    f.write('binwidth\terror\n')
    for i in xrange(n_binwidths):
        f.write('%8i\t%.10f\n' % (binwidths[i], errors[i]))
    f.close()
    # plot results
    if DoPlot:
        plt.clf()
        plt.semilogx(binwidths, errors, 'bo-', ms=8, clip_on=False)
        plt.xlabel('bin width',      fontsize=18)
        plt.ylabel('err ' + namevar, fontsize=18)
        plt.savefig(plotname, bbox_inches='tight')
        plt.close()
    obs_av = numpy.mean(obs)
    return binwidths, errors, obs_av
    
data = numpy.load("Grid Data/"+sys.argv[1])
bunching_v2(data, 2, "Observable",sys.argv[1]+"_bunching_results.txt",sys.argv[1]+"_bunching_plot.png",True)
