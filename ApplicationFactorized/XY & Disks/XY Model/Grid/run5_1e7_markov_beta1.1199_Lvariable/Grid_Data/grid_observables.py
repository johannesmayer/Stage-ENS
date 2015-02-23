import numpy, matplotlib.pylab as plt, sys


################################################################################


def autocorrelation(my_list, delta):
    mean = numpy.mean(my_list[delta:]*my_list[:-delta])
    return mean
    
    
    
    
################################################################################

if len(sys.argv) != 9:
    sys.exit("++++++++################ GIVE ME THE INPUT IN THE FOLLOWING ORDER: EVENT DATA : MARKOV DATA : EVENT THERMAL CUTOFF : MARKOV THERMAL CUTOFF : DT MIN : DT MAX : DT MIN FIT :MAXIMAL DELTA TO FIT ################+++++++++++++++")

event_data = numpy.load(sys.argv[1])     
markov_data = numpy.load(sys.argv[2])

event_thermal_cutoff = int(sys.argv[3])
markov_thermal_cutoff = int(sys.argv[4])

delta_min = int(sys.argv[5])
delta_max = int(sys.argv[6])

dt_min_fit = int(sys.argv[7])
dt_max_fit = int(sys.argv[8])

J = 1.
stepsize = 1

event_observable = []
event_correlator = []

markov_observable = []
markov_correlator = []

all_deltas = []


event_observable = event_data[event_thermal_cutoff:]
markov_observable = markov_data[markov_thermal_cutoff:]   

  
print 'avg ec ', numpy.mean(event_observable)
print 'avg mc ', numpy.mean(markov_observable)       
                       
event_observable = numpy.array(event_observable)
markov_observable = numpy.array(markov_observable)

event_mean = numpy.mean(event_observable)
event_sq_exp = numpy.mean(event_observable*event_observable)

markov_mean = numpy.mean(markov_observable)
markov_sq_exp = numpy.mean(markov_observable*markov_observable)


all_deltas = [0]
event_correlator = [1]
markov_correlator =[1]
if delta_min != 0:
    all_deltas = []
    event_correlator = []
    markov_correlator =[]

for delta in xrange(delta_min,delta_max,stepsize):
    print delta, delta_max
    all_deltas.append(delta)
    event_correlator.append((autocorrelation(event_observable,delta)-event_mean**2)/(event_sq_exp - event_mean**2))
    markov_correlator.append((autocorrelation(markov_observable,delta)-markov_mean**2)/(markov_sq_exp - markov_mean**2))

#plt.plot(event_observable,'r.')
event_tau_corr = 0.
marko_tau_corr = 0.
x = numpy.array(all_deltas[dt_min_fit:dt_max_fit])
event_log_y = numpy.log(event_correlator[dt_min_fit:dt_max_fit])
markov_log_y = numpy.log(markov_correlator[dt_min_fit:dt_max_fit])

# now fit the data with least square method

x = x[:, numpy.newaxis]

event_inv_tau,dummy1,dummy2,dummy3 = numpy.linalg.lstsq(x,-event_log_y)
markov_inv_tau, dum1, dum2, dum3 = numpy.linalg.lstsq(x,-markov_log_y)
if event_inv_tau[0]:
    event_tau_corr = 1.0/event_inv_tau[0]
else: event_tau_corr = float('inf')
if markov_inv_tau[0]:
    markov_tau_corr = 1.0/markov_inv_tau[0]
else: markov_tau_corr = float('inf')

print 'measured correlation time for ECEC: '+str(event_tau_corr)
print 'measured correlation time for MCMC: '+str(markov_tau_corr)
print "RATIO: "+str(markov_tau_corr/event_tau_corr)

event_tau_corr = 42.0

plt.plot(all_deltas,event_correlator,'r.', label='ECMC, tau= %f' %event_tau_corr)
plt.plot(all_deltas,markov_correlator,'b.', label='MCMC, tau = %f' %markov_tau_corr)

plt.plot(x, numpy.exp(-x/event_tau_corr),'r-',alpha=0.7, lw=3)
plt.plot(x, numpy.exp(-x/markov_tau_corr),'b-',alpha=0.7, lw=3)
plt.legend(loc = 'best')

plt.xlabel('Chains/Sweeps')
plt.ylabel('Autocorrelation Function')
plt.title('Autocorrelation of susceptibility data samples')

#plt.plot(all_deltas,markov_correlator,'b.')   
plt.yscale('log')
plt.show()