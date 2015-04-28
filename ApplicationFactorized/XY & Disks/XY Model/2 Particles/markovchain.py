import numpy, matplotlib.pyplot as plt, random

#####+#####+#####+#####+#####+##########+#####+#####+#####+#####+#####
def energy(J,delta_phi):
    ener = -J*numpy.cos(delta_phi)
    return ener
#####+#####+#####+#####+#####+##########+#####+#####+#####+#####+#####


beta = 1.0
J = 1.0
pi = numpy.pi

all_delta = []
all_energies = []

n_samples = 10**5

test_index = 0

L = 20.
clock = numpy.arange(0,5) * (2 * pi)/L
phi0, phi1 = [random.choice(clock),random.choice(clock)]
angles = [phi0, phi1]

step = 2 * pi / L
steps = (-step,step)

for index in xrange(n_samples):
    if (10*index) % n_samples == 0:
        print("PROGRESS: "+str(index)+"/"+str(n_samples))
        
    whomove = random.choice([0,1])
    move = random.choice(steps)
    delta = angles[0] - angles[1]
    dummy_delta = delta + (-1)**whomove * move
    if random.uniform(0.,1.) < min(1,numpy.exp(+beta*J*(numpy.cos(dummy_delta) - numpy.cos(delta)))):
        test_index += 1 
        angles[whomove] = (angles[whomove] + move ) % (2 * pi)        
    all_delta.append((angles[0] - angles[1]) % (2*pi))

#print all_delta

plt.hist(all_delta, bins=100, normed = True)
plt.show()


h,b = numpy.histogram(all_delta,bins = 100, normed = True)
b = 0.5 * (b[1:]+b[:-1])
plt.plot(b,h)
plt.plot(b,numpy.exp(numpy.cos(b))/7.95493)
plt.show()              


#numpy.save("2 Particle Data/markov_histogram.npy",all_delta)
