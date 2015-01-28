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
#*twopi

delta_phis = []
energies = []
test_histo = []

all_data = numpy.load("2 Particle Data/two_spins.npy")

for i_sweep in range(len(all_data)): 
    
    if i_sweep % 1000 == 0:
        print("PROGRESS: "+str(i_sweep)+"/"+str(len(all_data)))
        
# find out about who moves in each individual event chain and  
# calculate the average energy    
    data = all_data[i_sweep]     
    delta_phis.append((data[len(data)-1][0]-data[len(data)-1][1])%twopi)    
    

h,b = numpy.histogram(delta_phis,bins = 100, normed = True)
b = 0.5 * (b[1:]+b[:-1])
plt.plot(b,h)
plt.plot(b,numpy.exp(numpy.cos(b))/7.95493)
plt.show()    
    
    
    
    
    
    
    
    
    
    
    