import numpy, matplotlib.pylab as plt, sys


if len(sys.argv) != 5:
    sys.exit("PLEASE GIVE INPUT IN FORM: EVENT SUSCEPT. DATA : MARKOV SUSCEPT. DATA : EVENT THERMAL CUT : MCMC THERMAL CUT")

therm_ev_cut = int(sys.argv[3])
therm_mc_cut = int(sys.argv[4])

ev = numpy.load(sys.argv[1])[therm_ev_cut:]
ma = numpy.load(sys.argv[2])[therm_mc_cut:]

print 'a'

ev_hist, ev_binning = numpy.histogram(ev,bins=100,normed=True)
ma_hist, ma_binning = numpy.histogram(ma, bins=100, normed = True)
ev_hist = plt.hist(ev, ev_binning, normed= True, alpha=0.5, label='ECMC data')
#ma_hist = plt.hist(ma, ma_binning,normed=True, alpha = 0.5, label='markov data')
ma_hist = plt.hist(ma, ev_binning,normed=True, alpha = 0.5, label='markov data')

plt.title("Magnetic susceptibility histogram")
plt.xlabel('Magnetic susceptibility')
plt.ylabel('Frequency')

plt.legend(loc = 'best')

plt.show()