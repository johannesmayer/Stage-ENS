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

if len(sys.argv) != 3:
    sys.exit("++++++++################ GIVE ME THE INPUT IN THE FOLLOWING ORDER: EVENT DATA , MARKOV DATA ################+++++++++++++++")

event_data = numpy.load("Grid Data/"+sys.argv[1])     
markov_data = numpy.load("Grid Data/"+sys.argv[2])



J = 1.
delta_max = 500
stepsize = 1

event_energies = []
event_correlator = []

markov_energies = []
markov_correlator = []

all_deltas = []


for config in event_data:
    event_energies.append(energy_config(J,config)) 
for config in markov_data:
    markov_energies.append(energy_config(J,config))    
   
   
event_energies = numpy.array(event_energies)
markov_energies = numpy.array(markov_energies)

event_mean = numpy.mean(event_energies)
event_var = numpy.mean(event_energies*event_energies)

markov_mean = numpy.mean(markov_energies)
markov_var = numpy.mean(markov_energies*markov_energies)


print len(event_energies)

for delta in xrange(1,delta_max,stepsize):
    print delta
    all_deltas.append(delta)
    event_correlator.append((autocorrelation(event_energies,delta)-event_mean**2)/(event_var - event_mean**2))
    markov_correlator.append((autocorrelation(markov_energies,delta)-markov_mean**2)/(markov_var - markov_mean**2))

#plt.plot(event_energies,'r.')




plt.plot(all_deltas,event_correlator,'r.', label='ECMC')
plt.plot(all_deltas,markov_correlator,'b.', label='MCMC')

plt.xlabel('Delta Tau')
plt.ylabel('Autocorrelation Function')

#plt.plot(all_deltas,markov_correlator,'b.')   
plt.yscale('log')
plt.show()