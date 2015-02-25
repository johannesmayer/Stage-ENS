import numpy, matplotlib.pylab as plt, sys


################################################################################


def autocorrelation(my_list, delta):
    mean = numpy.mean(my_list[delta:]*my_list[:-delta])
    return mean
    
    
    
    
################################################################################

if len(sys.argv) != 6:
    sys.exit("++++++++################ GIVE ME THE INPUT IN THE FOLLOWING ORDER: EVENT DATA : cluster DATA : EVENT THERMAL CUTOFF : cluster THERMAL CUTOFF : MAXIMAL DELTA TO FIT ################+++++++++++++++")

event_data = numpy.load(sys.argv[1])     
cluster_data = numpy.load(sys.argv[2])

event_thermal_cutoff = int(sys.argv[3])
cluster_thermal_cutoff = int(sys.argv[4])

J = 1.
delta_max = 70
stepsize = 1

event_observable = []
event_correlator = []

cluster_observable = []
cluster_correlator = []

all_deltas = []


event_observable = event_data[event_thermal_cutoff:]
cluster_observable = cluster_data[cluster_thermal_cutoff:]   

  
print 'avg ec ', numpy.mean(event_observable)
print 'avg mc ', numpy.mean(cluster_observable)       
                       
event_observable = numpy.array(event_observable)
cluster_observable = numpy.array(cluster_observable)

event_mean = numpy.mean(event_observable)
event_sq_exp = numpy.mean(event_observable*event_observable)

cluster_mean = numpy.mean(cluster_observable)
cluster_sq_exp = numpy.mean(cluster_observable*cluster_observable)


all_deltas = [0]
event_correlator = [1]
cluster_correlator =[1]

for delta in xrange(1,delta_max,stepsize):
    print delta, delta_max
    all_deltas.append(delta)
    event_correlator.append((autocorrelation(event_observable,delta)-event_mean**2)/(event_sq_exp - event_mean**2))
    cluster_correlator.append((autocorrelation(cluster_observable,delta)-cluster_mean**2)/(cluster_sq_exp - cluster_mean**2))

#plt.plot(event_observable,'r.')
dt_max_fit = int(sys.argv[5])
event_tau_corr = 0.
marko_tau_corr = 0.
x = numpy.array(all_deltas[:dt_max_fit])
event_log_y = numpy.log(event_correlator[:dt_max_fit])
cluster_log_y = numpy.log(cluster_correlator[:dt_max_fit])

# now fit the data with least square method

x = x[:, numpy.newaxis]

event_inv_tau,dummy1,dummy2,dummy3 = numpy.linalg.lstsq(x,-event_log_y)
cluster_inv_tau, dum1, dum2, dum3 = numpy.linalg.lstsq(x,-cluster_log_y)
if event_inv_tau[0]:
    event_tau_corr = 1.0/event_inv_tau[0]
else: event_tau_corr = float('inf')
if cluster_inv_tau[0]:
    cluster_tau_corr = 1.0/cluster_inv_tau[0]
else: cluster_tau_corr = float('inf')

print 'measured correlation time for ECEC: '+str(event_tau_corr)
print 'measured correlation time for MCMC: '+str(cluster_tau_corr)
print "RATIO: "+str(cluster_tau_corr/event_tau_corr)

plt.plot(all_deltas,event_correlator,'r.-', label='ECMC, tau= %f' %event_tau_corr)
plt.plot(all_deltas,cluster_correlator,'b.-', label='CLUSTER, tau = %f' %cluster_tau_corr)

test_tau = 22.0

plt.plot(all_deltas,0.3*numpy.exp(-numpy.array(all_deltas)/test_tau),'g-',label='reference $\\tau$ = %f' %test_tau)

plt.plot(x, numpy.exp(-x/event_tau_corr),'r-',alpha=0.7, lw=3)
plt.plot(x, numpy.exp(-x/cluster_tau_corr),'b-',alpha=0.7, lw=3)
plt.legend(loc = 'best')

plt.xlabel('Chains/Sweeps')
plt.ylabel('Autocorrelation Function')
plt.title('Autocorrelation of susceptibility data samples')

#plt.plot(all_deltas,cluster_correlator,'b.')   
plt.yscale('log')
plt.show()