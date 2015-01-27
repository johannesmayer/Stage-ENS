import numpy, random, math, time, scipy.integrate as integrate


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

raw_data = numpy.load("2 Particle Data/two_spins.npy")

for i_sweep in range(len(raw_data)): 
    
    if i_sweep % 1000 == 0:
        print("PROGRESS: "+str(i_sweep)+"/"+str(len(raw_data)))
        
# find out about who moves in each individual event chain and  
# calculate the average energy    
    data = raw_data[i_sweep]     
    
    delta_phis.append(data[i_sweep][0]-data[i_sweep][1])    

for delta in delta_phis:
    energies.append(energy(delta,J))    
print numpy.mean(energies)
    
    
    
    
    
    
    
    
    
    
    
    