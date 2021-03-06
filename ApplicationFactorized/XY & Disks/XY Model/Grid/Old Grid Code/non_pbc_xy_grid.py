# -*- coding: utf-8 -*-
#2 spin XY model subroutine
#author: JM
#Date:  2015/02/03
import numpy, random, math, time

starting_time = time.time()

##################+ DEFINE ALL FUNCTIONS NEEDED IN THIS SECTION +##################

def energy(J,x):
    ene = -J*math.cos(x)
    return ene

def square_neighbors(L):
   N = L*L
   site_dic = {}
   x_y_dic = {}
   for j in range(N):
      row = j//L
      column = j-row*L
      site_dic[(row,column)] = j
      x_y_dic[j] = (row,column)
   nbr=[]
   for j in range(N):
       nbr.append([])
       row,column = x_y_dic[j]
       if column < L-1:
           right_nbr = site_dic[row,(column+1)]
           nbr[j].append(right_nbr)
       if row < L-1:
           up_nbr = site_dic[(row+1)%L,column]
           nbr[j].append(up_nbr)
       if column > 0:
           left_nbr = site_dic[row,(column-1)]
           nbr[j].append(left_nbr)
       if row > 0:
           down_nbr = site_dic[(row-1),column]
           nbr[j].append(down_nbr)
       nbr[j] = tuple(nbr[j])
   nbr = tuple(nbr)
   return nbr,site_dic,x_y_dic



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
##########+#########+##########+#########+##########+#########+##########+#########


L = 5
N = L*L

nbr, site_dic, x_y_dic = square_neighbors(L)


J = 1.0
beta = 10.0
pi = math.pi
twopi = 2*math.pi

energy_max = energy(J,math.pi)

all_collisions = []
chain_length = 100.*math.pi
n_times = 10**0


spins = [random.uniform(0,2.0*math.pi) for k in range(N)]

for i_sweep in range(n_times):
    if i_sweep % 1000 == 0:
        print("PROGRESS: "+str(i_sweep)+"/"+str(n_times))
    
    #resample the lifting variable and then move spins throught lattice
    total_displacement = 0.0
    lift = int(random.choice(numpy.arange(N)))
    these_collisions = []
    these_collisions.append(tuple([spins[:],lift,0]))
    
    
    while total_displacement < chain_length:
        
        # give a random energy to the lifting spin
        #check with whom he will be interacting
        neigh_deltas = [(spins[lift] - spins[nbr[lift][k]])%twopi for k in range(len(nbr[lift]))]
        distance_comparison = []
        energy_vault = []
        
        for number in neigh_deltas:
            #important to sample each neighbor individually
            upsilon=random.uniform(0.,1.)
            random_energy = (-1/beta)*math.log(upsilon)
            distance_comparison.append(calc_displacement(random_energy,J,number)[0])
            energy_vault.append(random_energy)
            
        whos_next = nbr[lift][numpy.argmin(distance_comparison)]
        delta_phi = neigh_deltas[numpy.argmin(distance_comparison)]
        used_energy = energy_vault[numpy.argmin(distance_comparison)]
        
        rest_displacement, n_turns = calc_displacement(used_energy, J, delta_phi)  
        displacement = n_turns*twopi + rest_displacement
        
        
        # see if displacement will exceed chain length and if yes truncate
        if displacement + total_displacement < chain_length:
            spins[lift] = (spins[lift]+displacement)%twopi
        else:
            displacement = chain_length - total_displacement
            spins[lift] = (spins[lift]+displacement)%twopi   
        total_displacement += displacement
        # see how often one can turn at max until one exceeds chain length
        while n_turns*twopi > (chain_length - total_displacement):
            n_turns -= 1
        #print total_displacement/pi
        lift = whos_next
        these_collisions.append(tuple([spins[:],lift,n_turns]))
        
    all_collisions.append(these_collisions[:])
numpy.save("Grid Data/non_pbc_xy_grid.npy",all_collisions)
