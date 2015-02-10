import numpy, math, matplotlib.pyplot as plt


#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####

def whos_lift(my_data):
    lift = 0
    if my_data[0][0][0] == my_data[1][0][0]:
        lift = 1
    return lift
    
#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####

twopi = 2*math.pi

all_delta_phi = numpy.load("2 Particle Data/event_chain.npy")
markov_chain = numpy.load("2 Particle Data/markov_histogram.npy")


                
histo1,b = numpy.histogram(all_delta_phi,bins = 100, normed = True)
markov_histo,k = numpy.histogram(markov_chain, bins = 100, normed = True)
                
b = 0.5 * (b[1:]+b[:-1])
k = 0.5 * (k[1:]+k[:-1])  

plt.plot(b,histo1,label="EVENT CHAIN")
plt.plot(k,markov_histo,label="MARKOV CHAIN")

maximal_distance = max(abs(histo1 - markov_histo))

print("MAXIMAL DISTANCE: "+str(maximal_distance))
plt.legend(loc=2)

plt.title("Comparison Event chain and regular MCMC")
plt.xlabel("Delta Phi")
plt.ylabel("Multiplicity")

plt.show()
                
                
                
                
                
                