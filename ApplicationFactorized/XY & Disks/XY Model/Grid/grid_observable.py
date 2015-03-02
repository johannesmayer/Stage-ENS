import numpy, matplotlib.pylab as plt, sys


################################################################################


def autocorrelation(my_list, delta):
    mean = numpy.mean(my_list[delta:]*my_list[:-delta])
    return mean
    
    
    
def energy_config(J,my_config):
    ene = 0.
    for delta_phi in my_config:
        ene -= J*numpy.cos(delta_phi)
    return ene
    
################################################################################

if len(sys.argv) != 4:
    sys.exit("++++++++################ GIVE ME THE INPUT IN THE FOLLOWING ORDER: EVENT DATA : EVENT THERMAL CUTOFF : MAXIMAL DELTA TO FIT ################+++++++++++++++")

data = numpy.load(sys.argv[1])     

thermal_cutoff = int(sys.argv[2])
J = 1.
delta_max = 250
stepsize = 1

observable = []
correlator = []


all_deltas = []


observable = data[thermal_cutoff:]

  
print 'avg ec ', numpy.mean(observable)
                       
observable = numpy.array(observable)

mean = numpy.mean(observable)
sq_exp = numpy.mean(observable*observable)



all_deltas = [0]
correlator = [1]

for delta in xrange(1,delta_max,stepsize):
    all_deltas.append(delta)
    correlator.append((autocorrelation(observable,delta)-mean**2)/(sq_exp - mean**2))

#plt.plot(observable,'r.')
dt_max_fit = int(sys.argv[3])
tau_corr = 0.
marko_tau_corr = 0.
x = numpy.array(all_deltas[:dt_max_fit])
log_y = numpy.log(correlator[:dt_max_fit])

# now fit the data with least square method

x = x[:, numpy.newaxis]

inv_tau,dummy1,dummy2,dummy3 = numpy.linalg.lstsq(x,-log_y)
if inv_tau[0]:
    tau_corr = 1.0/inv_tau[0]
else: tau_corr = float('inf')

print 'measured correlation time for ECEC: '+str(tau_corr)

plt.plot(all_deltas,correlator,'r.', label='ECMC, tau= %f' %tau_corr)

plt.plot(x, numpy.exp(-x/tau_corr),'r-',alpha=0.7, lw=3)
plt.legend()

plt.xlabel('Chains/Sweeps')
plt.ylabel('Autocorrelation Function')
plt.title('Autocorrelation of energy data samples')

#plt.plot(all_deltas,markov_correlator,'b.')   
plt.yscale('log')
plt.show()