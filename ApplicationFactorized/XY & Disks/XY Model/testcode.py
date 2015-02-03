# -*- coding: utf-8 -*-
#2 spin XY model subroutine
#author: JM
import numpy as np, random, math, time, sys

starting_time = time.time()

##################+ DEFINE ALL FUNCTIONS NEEDED IN THIS SECTION +##################

def energy(J,x):
    ene = -J*math.cos(x)
    return ene

#constructing a square lattice

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


#for a given set of spins calculate all delta phis

def all_angles(my_spins, nbr):
    N = len(my_spins)
    all_delta_phi = []    
    for index in range(N):
        for neigh in nbr[index]:
            all_delta_phi.append(abs(my_spins[index]-my_spins[neigh]))
    all_delta_phi = np.unique(all_delta_phi)
    return list(all_delta_phi)
##########+#########+##########+#########+##########+#########+##########+#########


# initialize the grit one is working on
all_data = np.load("Grid Data/xy_grid.npy")
number_of_chains = len(all_data)


N = int(len(all_data[0][0][0]))
L = int(math.sqrt(float(N)))

nbr, site_dic, x_y_dic = square_neighbors(L)

pi = math.pi
twopi = 2*math.pi

delta_step = 0.1*pi

for chain in xrange(number_of_chains):   
    data = all_data[chain]
    #of the current start of the chain take all the delta phis
    current_delta_list = all_angles(data[0][0],nbr)

    for index in range(len(data)-1):
        lift = data[index][1]
        n_turns = data[index][2]
        rest = 0.
    #then for the moving one take out all the neighboring delta phis
        for neighbor in nbr[lift]:
            neigh_delta = abs(data[0][0][neighbor]-data[0][0][lift])
            for element in current_delta_list:
                if abs(element - neigh_delta) == 0:
                    current_delta_list.remove(element)
        phi_from = data[index][0][lift]
        phi_to = data[index+1][0][lift]
        
        if (phi_from + rest)% twopi > phi_to:
            rest = (phi_from + rest )%twopi - phi_to
            continue
        else: phi_from += rest
        if phi_to < phi_from:
            phi_to += twopi
        phi_from = phi_from + rest
        phi_to = phi_to + twopi*n_turns
        phi_still = [data[index][0][nbr[lift][j]] for j in range(4)]
        
            
               
                
                
    
print("DURATION: "+str(time.time()-starting_time))

