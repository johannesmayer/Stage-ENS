# -*- coding: utf-8 -*-
#2 spin XY model subroutine
#author: JM
import numpy as np, random, math, time, sys, matplotlib.pyplot as plt

starting_time = time.time()

##################+ DEFINE ALL FUNCTIONS NEEDED IN THIS SECTION +##################

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
            direct_dist = abs((my_spins[index]-my_spins[neigh]))
            all_delta_phi.append(min(direct_dist, twopi -direct_dist))
    all_delta_phi = np.unique(all_delta_phi)
    return list(all_delta_phi)
    
def map_periodic_distance(my_list):
    length = len(my_list)
    for index in xrange(length):
        my_list[index] = min(my_list[index],twopi-my_list[index])
    return my_list
    
def periodic_distance(spin0,spin1):
    dir_dist = abs(spin0-spin1)
    per_dist = min(dir_dist, twopi-dir_dist)
    return per_dist
    
        
##########+#########+##########+#########+##########+#########+##########+#########


if len(sys.argv) != 2:
    sys.exit("+++++++++ GIVE ME THE FOLLOWING INPUT: NAME OF NPY FILE WITH COLLISION POINTS OF XY GRID ++++++++++++++")

#import the data
all_data = np.load("Grid Data/"+sys.argv[1])
number_of_chains = len(all_data)

sampled_configurations = []

N = int(len(all_data[0][0][0]))
L = int(math.sqrt(float(N)))

nbr, site_dic, x_y_dic = square_neighbors(L)

pi = math.pi
twopi = 2*math.pi

#delta_step = 0.02*pi


for chain in xrange(number_of_chains):  
    if chain % 1000 == 0:
        print chain, number_of_chains 
    
    data = all_data[chain]
    final_config = data[len(data)-1][0]
    #print final_config
    #look_at = random.randrange(N)
    #neigh = random.choice(nbr[look_at])
    #sampled_configurations.append(periodic_distance(final_config[look_at],final_config[neigh]))
    final_deltas = all_angles(final_config, nbr)
    final_deltas = map_periodic_distance(final_deltas)
    sampled_configurations.append(final_deltas)
  
np.save("Grid Data/delta_phis_of_"+sys.argv[1],sampled_configurations)       

print("DURATION: "+str(time.time()-starting_time))
                
    

