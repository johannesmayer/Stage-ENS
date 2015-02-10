import numpy, math, matplotlib.pyplot as plt, random

#####+#####+#####+#####+#####+##########+#####+#####+#####+#####+#####
def energy(J,delta_phi):
    ener = -J*math.cos(delta_phi)
    return ener
#####+#####+#####+#####+#####+##########+#####+#####+#####+#####+#####


beta = 1.0
J = 1.0
pi = math.pi


all_delta = []
all_energies = []
delta_phi = random.uniform(0.,2*pi)

step= 1*pi

n_samples = 10**7

test_index = 0

for index in xrange(n_samples):
    if index % 10000 == 0:
        print("PROGRESS: "+str(index)+"/"+str(n_samples))
        
    jump = random.uniform(-step,step)
    
    if random.uniform(0.,1.) < min(1,math.exp(-beta*(energy(J,delta_phi+jump)-energy(J,delta_phi)))):
        test_index += 1 
        delta_phi = (delta_phi + jump) % (2*pi)
        
    all_delta.append(delta_phi) 

#print all_delta

"""
h,b = numpy.histogram(all_delta,bins = 100, normed = True)
b = 0.5 * (b[1:]+b[:-1])
plt.plot(b,h)
plt.plot(b,numpy.exp(numpy.cos(b))/7.95493)
plt.show()              
"""

numpy.save("2 Particle Data/markov_histogram.npy",all_delta)
