# -*- coding: utf-8 -*-
#2 spin XY model subroutine
#author: JM
import numpy as np, random, math, time, sys, matplotlib.pyplot as plt

starting_time = time.time()

##################+ DEFINE ALL FUNCTIONS NEEDED IN THIS SECTION +##################

def energy(J,move_spin_,nbrs_,spins_):
    ene = 0.0
    for neigh in nbrs_:
        ene += -J*math.cos(move_spin_-spins_[neigh])
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
            all_delta_phi.append(min(abs(my_spins[index]-my_spins[neigh]),twopi - abs(my_spins[index]-my_spins[neigh]) ))
    all_delta_phi = np.unique(all_delta_phi)
    return list(all_delta_phi)

def periodic_distance(spin0,spin1):
    dir_dist = abs(spin0-spin1)
    per_dist = min(dir_dist, twopi-dir_dist)
    return per_dist
    
########################+#######################+###########################+

L=3
N=L*L

pi = math.pi
twopi = 2*math.pi

J = 1.0
beta = 1.0
step = 1.*pi

nbr, site_dic, x_y_dic = square_neighbors(L)

spins = [random.uniform(0,2*pi) for k in xrange(N)]
all_configurations = []
all_delta_phis = []
successor = 0.

n_times = 10**6

for i_sweep in xrange(n_times):
    
    if i_sweep % 10000 == 0:
        print i_sweep,n_times
    for index in xrange(N):
        who_moves = random.choice(np.arange(N))
        neighs = nbr[who_moves]
        moved_spin = spins[who_moves]
        move = random.uniform(-step,step)
        if random.uniform(0.,1.) < math.exp(-beta*(energy(J,moved_spin+move,neighs,spins)-energy(J,moved_spin,neighs,spins))):
            spins[who_moves] = (spins[who_moves] + move)%twopi
            successor += 1
    all_configurations.append(spins[:])   

print len(all_configurations)
for config in all_configurations:
    look_at = random.choice(np.arange(N))
    which_neigh = random.choice(nbr[look_at])
    all_delta_phis.append(periodic_distance(config[look_at],config[which_neigh]))
    #all_delta_phis.extend(all_angles(config,nbr))
print("RATE: "+str(successor/n_times/N))
    
np.save("Grid Data/grid_markov_data.npy",all_delta_phis)
"""
h,b = np.histogram(all_delta_phis,bins = 100, normed = False)

b = 0.5*(b[1:]+b[:-1])
plt.subplot(221)
plt.plot(b,h)

plt.show() 
"""    