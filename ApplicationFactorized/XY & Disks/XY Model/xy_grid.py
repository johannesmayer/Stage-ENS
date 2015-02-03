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
      row,column = x_y_dic[j]
      right_nbr = site_dic[row,(column+1)%L]
      up_nbr = site_dic[(row+1)%L,column]
      left_nbr = site_dic[row,(column-1+L)%L]
      down_nbr = site_dic[(row-1+L)%L,column]
      nbr.append((right_nbr,up_nbr,left_nbr,down_nbr))
   nbr = tuple(nbr)
   return nbr,site_dic,x_y_dic

def calc_displacement(random_energy,J,delta_phi):
    valley_crossing_number = random_energy // (2*J)
    rest_energy = random_energy % (2*J)
    displacement = 0.0

    delta_phi = delta_phi % twopi
    phi_bullet = 0
    phi_star = 0
            
    if delta_phi > math.pi and delta_phi < twopi:
        #go down into the valley and see how far up you come
        phi_bullet = twopi - delta_phi
        phi_star = math.acos(1-rest_energy/J)  
            
    else:
        if energy_max-energy(J,delta_phi) > rest_energy:
            phi_star = math.acos(math.cos(delta_phi) - rest_energy/J) - delta_phi
        else:             
            phi_star = twopi - delta_phi + math.acos(1-(rest_energy - energy_max + energy(J,delta_phi))/J)
                
    displacement = phi_bullet + phi_star + valley_crossing_number*twopi
    return displacement, valley_crossing_number        
##########+#########+##########+#########+##########+#########+##########+#########


L = 3
N = L*L

nbr, site_dic, x_y_dic = square_neighbors(L)

J = 1.0
beta = 15.0
twopi = 2*math.pi

energy_max = energy(J,math.pi)

all_collisions = []
chain_length = 0.2*math.pi
n_times = 10**1


spins = [random.uniform(0,0.1*math.pi) for k in range(N)]

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
        upsilon=random.uniform(0.,1.)
        random_energy = (-1/beta)*math.log(upsilon)
        #check with whom he will be interacting
        all_deltas = [(spins[lift] - spins[nbr[lift][k]])%twopi for k in range(4)]
        whos_next = nbr[lift][numpy.argmin(all_deltas)]
        
        delta_phi = min(all_deltas)
        
        rest_displacement, n_turns = calc_displacement(random_energy, J, delta_phi)  
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
    
        lift = whos_next
        these_collisions.append(tuple([spins[:],lift,n_turns]))
        
    all_collisions.append(these_collisions[:])

numpy.save("Grid Data/xy_grid.npy",all_collisions)