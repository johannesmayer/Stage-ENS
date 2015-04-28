import math, numpy, random, matplotlib.pyplot as plt

J = 1.0
beta = 1.0


def energy(J,x):
    ene = -J*math.cos(x)
    return ene
    
def calc_displacement(random_energy,J,delta_phi):
    del_phi = delta_phi % twopi
    valley_crossing_number = random_energy // (2*J)
    rest_energy = random_energy % (2*J)
    displacement = 0.0

    phi_bullet = 0
    phi_star = 0
            
    if del_phi > math.pi and del_phi < twopi:
        #go down into the valley and see how far up you come
        phi_bullet = twopi - del_phi
        phi_star = math.acos(1-rest_energy/J)  
            
    else:
        if energy_max-energy(J,del_phi) > rest_energy:
            phi_star = math.acos(math.cos(del_phi) - rest_energy/J) - del_phi
        else:             
            phi_star = twopi - del_phi + math.acos(1-(rest_energy - energy_max + energy(J,del_phi))/J)
                
    displacement = phi_bullet + phi_star + valley_crossing_number*twopi
    return displacement, valley_crossing_number  
    
pi = numpy.pi
twopi = 2*pi 
    
energy_max = energy(J,math.pi)
chain_length = 2*pi


N = 2


n_times = 10**2


spins = [random.uniform(0,2*pi) for k in range(N)]
all_delta_phi = []

for i_sweep in range(n_times):
    if (i_sweep*100) % n_times == 0 and i_sweep != 0:
        percentage = i_sweep * 100 / n_times
        print percentage           
    #resample the lifting variable and then move spins throught lattice
    total_displacement = 0.0
    lift = random.randrange(N)
    #the first point in each chain is the starting point+who will move next
    moves_this_chain = 0 
    
    while total_displacement < chain_length:
        moves_this_chain += 1
        # give a random energy to the lifting spin
        #check with whom he will be interacting
        neigh_deltas = [(spins[lift] - spins[(lift + 1)%2])%twopi]
        distance_comparison = []
        energy_vault = []
        
        for number in neigh_deltas:
                #important to sample each neighbor individually
                upsilon = random.uniform(0.,1.)
                random_energy = (-1/beta)*math.log(upsilon)
                distance_comparison.append(calc_displacement(random_energy,J,number)[0])
                energy_vault.append(random_energy)
                
        whos_next = (lift + 1 )%2
        delta_phi = neigh_deltas[numpy.argmin(distance_comparison)]
        used_energy = energy_vault[numpy.argmin(distance_comparison)]       
            
        rest_displacement, n_turns = calc_displacement(used_energy, J, delta_phi)  
        displacement = n_turns*twopi + rest_displacement
            
        if displacement + total_displacement < chain_length:
            spins[lift] = (spins[lift]+displacement)%twopi
            
        else:
            displacement = chain_length - total_displacement
            spins[lift] = (spins[lift]+displacement)%twopi  
            all_delta_phi.append( (spins[lift] - spins[(lift + 1)%2])%(twopi) )
        total_displacement += displacement
        lift = whos_next

            
            
plt.hist(all_delta_phi, bins = 100, normed = True, alpha = 0.7)   
h , b = numpy.histogram(all_delta_phi, bins = 100, normed = True)
binning = 0.5*(b[1:]+b[:-1])
plt.plot(binning,numpy.exp(beta*J*numpy.cos(binning))/7.95,'r', lw = 2)
print binning
plt.show()
         
            