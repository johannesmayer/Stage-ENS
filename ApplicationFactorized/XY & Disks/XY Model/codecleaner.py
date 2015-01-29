import numpy, random, math, time, matplotlib.pyplot as plt


#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####

def whos_lift(my_data):
    lift = 0
    if my_data[0][0] == my_data[1][0]:
        lift = 1
    return lift
    
def energy(delta_phi,J):
    ene = -J*math.cos(delta_phi)
    return ene
    
    
#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####
J = 1    
twopi = 2*math.pi

angle_step = 0.2


delta_phis = []
energies = []
test_histo = []

all_data = numpy.load("2 Particle Data/two_spins.npy")

for i_sweep in xrange(len(all_data)): 
    
    if i_sweep % 1000 == 0:
        print("PROGRESS: "+str(i_sweep)+"/"+str(len(all_data)))
        
    data = all_data[i_sweep]     
    who_lift = whos_lift(data)
    for index in xrange(len(data)-1):
        phi_still = data[index][(who_lift+1)%2]
        phi_from = data[index][who_lift]
        phi_to = data[index+1][who_lift]
        if phi_to < phi_from:
            phi_to = phi_to + twopi
        
    print who_lift    

h,b = numpy.histogram(delta_phis,bins = 100, normed = True)
b = 0.5 * (b[1:]+b[:-1])
plt.plot(b,h)
plt.plot(b,numpy.exp(numpy.cos(b))/7.95493)
plt.show()    
    
    
    
    
    
    
    
    
    
    
    