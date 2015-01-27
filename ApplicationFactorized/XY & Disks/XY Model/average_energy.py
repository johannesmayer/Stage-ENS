import numpy, random, math, time, scipy.integrate as integrate



def integrand(x,y,J):
    return -J*math.cos(x-y)

def avg_energy(phi_0, phi_0_new, phi_1,J):
    length = abs(phi_0 - phi_0_new)
    phi_0_to = phi_0_new
    if phi_0 > phi_0_to:
        #print("GOOD CALL")
        phi_0_to = phi_0_to + 2*math.pi
    if length != 0:
        ene = integrate.quad(integrand,phi_0,phi_0_to,args =(phi_1,J))[0]/length
    else: ene = 0
    return ene

def whos_lift(my_data):
    lift = 0
    if my_data[0][0] == my_data[1][0]:
        lift = 1
    return lift
    
#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####
J = 1    
raw_data = numpy.load("2 Particle Data/two_spins.npy")
average_energies = []
for i_sweep in range(len(raw_data)): 
    
    if i_sweep % 1000 == 0:
        print("PROGRESS: "+str(i_sweep)+"/"+str(len(raw_data)))
    
# find out about who moves in each individual event chain and  
# calculate the average energy    
    data = raw_data[i_sweep]     
    lift = whos_lift(data)
    for index in range(len(data)-1):
        phi_still = data[index][(lift+1)%2]
        phi_move_from = data[index][lift]
        phi_move_to = data[index+1][lift]
        ener = avg_energy(phi_move_from, phi_move_to, phi_still,J)
        average_energies.append(ener)
        lift = (lift+1)%2
        
    
    
print numpy.mean(average_energies)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    