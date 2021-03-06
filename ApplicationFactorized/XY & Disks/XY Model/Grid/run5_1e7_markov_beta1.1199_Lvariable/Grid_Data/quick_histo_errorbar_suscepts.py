import numpy, matplotlib.pylab as plt, sys, math, os

def err_independent(obs):
    """
    Error on the average for a set of independent samples.
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
    obs_av   = numpy.mean(obs)
    errors   = [err_independent(obs)]
    old_list = []
    new_list = [i for i in obs]
    for l in xrange(1, n_binwidths):
       # one binning step
       old_list = new_list[:]
       elements_left = len(old_list)
       new_list = []
       while elements_left > base:
          new_list.append(sum(old_list.pop() for i in xrange(base)) / float(base))
          elements_left -= base
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
    return binwidths, errors, obs_av

def naive_look_for_converged_error(errors):
    """
    This function is an *extremely* naive way of checking whether a plateau has
    been reached (just looking for the first non-increase in the error list).
    Use at your own risk (it is always better to check the plot by yourself).
    """
    for i in xrange(len(errors) - 1):
        if errors[i] >= errors[i + 1]:
            return errors[i]
    return errors[-1]

def histogram_with_errors(x, nbins, base, ID, limits=[]):
    """
    Function performing bunching on every bin of the histogram.
    Input:
      x      : array of samples
      nbins  : number of bins
      base   : bin widths are taken to be 1, base, base^2, base^3..
      ID     : identifying string
      limits : min/max values for the histogram (optional)
    Output:
      bin_centres = array with centres of bins
      h = array with the frequencies
      h_err = naive errros of each bin 
    
    
    """
    # numpy-fy observable
    if type(x) is list:
        x = numpy.array(x)
    # define file/folder names
    name_output = ID + '.dat'
    out_dir = 'data_binning_' + ID + '/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    # define bins
    if limits:
        xmin, xmax = limits
    else:
        xmin, xmax = numpy.amin(x) - 1e-12, numpy.amax(x) + 1e-12
    bin_edges = numpy.linspace(xmin, xmax, nbins + 1)
    print bin_edges
    bin_width = bin_edges[1] - bin_edges[0]
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    print '[histo_with_err] #data:           %i' % x.shape[0]
    print '[histo_with_err] #bins:           %i' % nbins
    print '[histo_with_err] binning base:    %i' % base
    print '[histo_with_err] histo bin width: %f' % bin_width
    # perform bunching for each bin
    h, h_err = [], []
    out = open(name_output, 'w')
    print '[histo_with_err] start error analysis for each bin'
    for k in xrange(nbins):
        binned_x = numpy.logical_and(x > bin_edges[k], x < bin_edges[k + 1])
        dummy1, errors, av = bunching_v2(binned_x, base, 'bin %i' % k,
                               out_dir + 'data_bin_%03i.dat' % k,
                               out_dir + 'plot_bin_%03i.png' % k, DoPlot=True)
        err = naive_look_for_converged_error(errors)
        av  /= bin_width
        err /= bin_width
        h.append(av)
        h_err.append(err)
        out.write('%.12f %.12f %.12f\n' % (bin_centers[k], av, err))
        out.flush()
        print 'bin %3i: %.6f +/- %.6f (%.2f %%)' % (k, av, err, err * 100.0 / av)
    out.close()
    # do plot
    plt.clf()
    plt.errorbar(bin_centers, h, yerr=h_err)
    plt.xlim(xmin * 0.999, xmax * 1.001)
    plt.title('%s' % ID)
    plt.grid()
    plt.savefig('plot_' + ID + '.png', bbox_inches='tight')
    plt.close()
    return bin_centers, h , h_err


if len(sys.argv) != 5:
    sys.exit("PLEASE GIVE INPUT IN FORM: EVENT SUSCEPT. DATA : MARKOV SUSCEPT. DATA : EVENT THERMAL CUT : MCMC THERMAL CUT")

therm_ev_cut = int(sys.argv[3])
therm_mc_cut = int(sys.argv[4])

ev_data = numpy.load(sys.argv[1])[therm_ev_cut:]
ma_data = numpy.load(sys.argv[2])[therm_mc_cut:]




print 'a'



ev_bin_centers, ev_histo, ev_histo_errors = histogram_with_errors(ev_data, 100, 10, 'Event Chain Data', limits=[])
mar_bin_centers, mar_histo, mar_histo_errors = histogram_with_errors(ma_data, 100, 10, 'Markov Chain Data', limits=[])


plt.clf()
plt.errorbar(ev_bin_centers, ev_histo, yerr=ev_histo_errors, label='ECMC', alpha=0.5)
plt.errorbar(mar_bin_centers, mar_histo, yerr=mar_histo_errors, label='ECMC', alpha=0.5)

plt.xlim(min(ev_bin_centers) * 0.999, max(ev_bin_centers)  * 1.001)
plt.grid()

plt.show()

plt.xlabel('Magnetic susceptibility')
plt.ylabel('Frequency')

plt.legend()

plt.show()