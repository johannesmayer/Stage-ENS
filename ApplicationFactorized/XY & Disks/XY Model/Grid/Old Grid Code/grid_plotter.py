import numpy, math, matplotlib.pyplot as plt


#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####

def whos_lift(my_data):
    lift = 0
    if my_data[0][0][0] == my_data[1][0][0]:
        lift = 1
    return lift
    
#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####

twopi = 2*math.pi

#event_chain_delta_phi = numpy.load("Grid Data/event_chain.npy")

#event_chain_delta_phi = numpy.load("Grid Data/grid_event_chain.npy")
#end_chain_delta_phi = numpy.load("Grid Data/grid_end_chain_data.npy")
end_chain_delta_phi = numpy.load("Grid Data/grid_end_chain_data_all_deltas.npy")
markov_chain_delta_phi = numpy.load("Grid Data/grid_markov_data.npy")


                
                
#plt.hist(event_chain_delta_phi,bins=100,normed = True,alpha=0.5,label="EVENT CHAIN")
#b = numpy.histogram(end_chain_delta_phi, bins=100)[1]
plt.hist(end_chain_delta_phi,bins=100,normed = True,alpha=0.5,label="END CHAIN")
plt.hist(markov_chain_delta_phi,bins=100,normed = True,alpha=0.5,label="MARKOV CHAIN")


#b = 0.5*(b[1:]+b[:-1])

#plt.plot(b,numpy.exp(numpy.cos(b))/3.97746)
#maximal_distance = max(abs(event_chain_delta_phi - markov_chain_delta_phi))

#print("MAXIMAL DISTANCE: "+str(maximal_distance))
plt.legend(loc=1)

plt.title("Comparison Event chain and regular MCMC")
plt.xlabel("Delta Phi")
plt.ylabel("Multiplicity")

plt.show()
                
                
                
                
                
                