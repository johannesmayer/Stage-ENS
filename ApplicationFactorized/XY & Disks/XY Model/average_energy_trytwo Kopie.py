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

raw_data = numpy.load("2 Particle Data/two_spins.npy")

for i_sweep in range(len(raw_data)): 
    
    if i_sweep % 1000 == 0:
        print("PROGRESS: "+str(i_sweep)+"/"+str(len(raw_data)))
    
# find out about who moves in each individual event chain and  
# calculate the average energy    
    data = raw_data[i_sweep]     
    lift = whos_lift(data)
    rest = 0
    for index in range(len(data)-1):
        phi_still = data[index][(lift+1)%2]
        phi_move_from = data[index][lift]
        phi_move_to = data[index+1][lift]
        angle = phi_move_from + rest
        delta_phis.append((angle - phi_still)%twopi)

        if phi_move_to < phi_move_from:
            phi_move_to += twopi
        while angle < phi_move_to:
            if angle+angle_step < phi_move_to:
                angle += angle_step 
                delta_phis.append((angle - phi_still)%twopi)
            else:
                angle = phi_move_to
                rest = angle-angle_step-phi_move_to
                lift = (lift+1)%2
                continue

for delta in delta_phis:
    energies.append(energy(delta,J))

print numpy.mean(energies)    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    