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

if len(sys.argv) != 8:
    sys.exit("++++++++################ GIVE ME THE INPUT IN THE FOLLOWING ORDER: PLUS DATA : MMINUS DATA : ZERO DATA :  PLUS THERMAL CUTOFF : MINUS THERMAL CUTOFF : ZERO THERMAL CUTOFF MAXIMAL DELTA TO FIT ################+++++++++++++++")

plus_data = numpy.load("Grid_Data/"+sys.argv[1])     
minus_data = numpy.load("Grid_Data/"+sys.argv[2])
zero_data = numpy.load("Grid_Data/"+sys.argv[3])


plus_thermal_cutoff = int(sys.argv[4])
minus_thermal_cutoff = int(sys.argv[5])
zero_thermal_cutoff = int(sys.argv[6])


J = 1.
delta_max = 500
stepsize = 1

plus_observable = []
plus_correlator = []

minus_observable = []
minus_correlator = []

zero_observable = []
zero_correlator = []


all_deltas = []

plus_observable = plus_data[plus_thermal_cutoff:]
minus_observable = minus_data[minus_thermal_cutoff:]   
zero_observable = zero_data[zero_thermal_cutoff:]   

  
print 'avg ec ', numpy.mean(plus_observable)
print 'avg mc ', numpy.mean(minus_observable)       
                       
plus_observable = numpy.array(plus_observable)
minus_observable = numpy.array(minus_observable)
zero_observable = numpy.array(zero_observable)



plus_mean = numpy.mean(plus_observable)
plus_sq_exp = numpy.mean(plus_observable*plus_observable)

minus_mean = numpy.mean(minus_observable)
minus_sq_exp = numpy.mean(minus_observable*minus_observable)

zero_mean = numpy.mean(zero_observable)
zero_sq_exp = numpy.mean(zero_observable*zero_observable)


all_deltas = [0]

plus_correlator = [1]
minus_correlator =[1]
zero_correlator =[1]




for delta in xrange(1,delta_max,stepsize):
    all_deltas.append(delta)
    plus_correlator.append((autocorrelation(plus_observable,delta)-plus_mean**2)/(plus_sq_exp - plus_mean**2))
    minus_correlator.append((autocorrelation(minus_observable,delta)-minus_mean**2)/(minus_sq_exp - minus_mean**2))
    zero_correlator.append((autocorrelation(zero_observable,delta)-zero_mean**2)/(zero_sq_exp - zero_mean**2))

#plt.plot(plus_observable,'r.')
dt_max_fit = int(sys.argv[7])
plus_tau_corr = 0.
minus_tau_corr = 0.
zero_tauz_corr = 0.
x = numpy.array(all_deltas[:dt_max_fit])
plus_log_y = numpy.log(plus_correlator[:dt_max_fit])
minus_log_y = numpy.log(minus_correlator[:dt_max_fit])
zero_log_y = numpy.log(zero_correlator[:dt_max_fit])

# now fit the data with least square method
"""
x = x[:, numpy.newaxis]

plus_inv_tau,dummy1,dummy2,dummy3 = numpy.linalg.lstsq(x,-plus_log_y)
minus_inv_tau, dum1, dum2, dum3 = numpy.linalg.lstsq(x,-minus_log_y)
zero_inv_tau, dum1, dum2, dum3 = numpy.linalg.lstsq(x,-zero_log_y)

if plus_inv_tau[0]:
    plus_tau_corr = 1.0/plus_inv_tau[0]
else: plus_tau_corr = float('inf')
if minus_inv_tau[0]:
    minus_tau_corr = 1.0/minus_inv_tau[0]
else: minus_tau_corr = float('inf')
if zero_inv_tau[0]:
    zero_tau_corr = 1.0/zero_inv_tau[0]
else: zero_tau_corr = float('inf')

print 'measured correlation time for ECEC: '+str(plus_tau_corr)
print 'measured correlation time for MCMC: '+str(minus_tau_corr)
print 'measured correlation time for MCMC: '+str(zero_tau_corr)

"""
plt.plot(all_deltas,plus_correlator,'r.',label = 'plus')
plt.plot(all_deltas,minus_correlator,'b.', label = 'minus')
plt.plot(all_deltas,zero_correlator,'g.', label = 'zero')

"""
plt.plot(x, numpy.exp(-x/plus_tau_corr),'r-',alpha=0.7, lw=3)
plt.plot(x, numpy.exp(-x/minus_tau_corr),'b-',alpha=0.7, lw=3)
plt.legend()
"""
plt.legend(loc='best')
plt.xlabel('Chains/Sweeps')
plt.ylabel('Autocorrelation Function')
plt.title('Autocorrelation of energy data samples')

plt.yscale('log')
plt.show()