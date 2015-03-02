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

if len(sys.argv) != 5:
    sys.exit("++++++++################ GIVE ME THE INPUT IN THE FOLLOWING ORDER: EVENT DATA : EVENT THERMAL CUTOFF ################+++++++++++++++")

thermal_cutoff = int(sys.argv[4])

data0 = numpy.load(sys.argv[1])[thermal_cutoff:]
data1 = numpy.load(sys.argv[2])[thermal_cutoff:]
data2 = numpy.load(sys.argv[3])[thermal_cutoff:]    

data = [data0, data1, data2]

J = 1.
delta_max = 50
stepsize = 1

observable = []
correlator = []


all_deltas = []
i = 0
tau_ec = 22.0
tau_mc = 240.0
tau_cl = 4.5
names = ['MCMC','ECMC','CLUSTER']
taus = [tau_mc, tau_ec, tau_cl]

for observable in data:
    
    print 'avg ec ', numpy.mean(observable)
                        
    observable = numpy.array(observable)
    
    mean = numpy.mean(observable)
    sq_exp = numpy.mean(observable*observable)
    
    all_deltas = [0]
    correlator = [1]
    
    for delta in xrange(1,delta_max,stepsize):
        all_deltas.append(delta)
        correlator.append((autocorrelation(observable,delta)-mean**2)/(sq_exp - mean**2))
    
    plt.plot(all_deltas,correlator, label=names[i]+'$\\tau$ =' +str(taus[i]) )    
    i +=1

all_deltas = numpy.array(all_deltas)

plt.plot(all_deltas,0.3*numpy.exp(-all_deltas / tau_ec),'g+')
plt.plot(all_deltas,numpy.exp(-all_deltas / tau_mc),'b+')
plt.plot(all_deltas,numpy.exp(-all_deltas / tau_cl),'r+')


plt.legend(loc = 'best')    
plt.xlabel('Chains/Sweeps/Clusterupdates')
plt.ylabel('Autocorrelation Function')
plt.title('Autocorrelation of pbservable data samples')
    
plt.yscale('log')
plt.show()