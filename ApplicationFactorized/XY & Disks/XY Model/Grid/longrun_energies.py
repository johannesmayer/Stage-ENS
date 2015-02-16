# -*- coding: utf-8 -*-
#2 spin XY model subroutine
#author: JM
import numpy as np, random, math, time, sys, matplotlib.pyplot as plt

starting_time = time.time()

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


def make_bonds(N,nbr):
    bonds = []
    for particle in xrange(N):
        for neigh in nbr[particle]:
            this_bond = [particle, neigh]
            this_bond = sorted(this_bond)
            bonds.append(tuple(this_bond))
    bonds = np.unique(bonds)
    return bonds

#for a given set of spins calculate all delta phis
def grid_energy(J,my_config,bonds):
    ene = 0.
    my_deltas = all_angles(my_config, bonds)
    for angle in my_deltas:
        ene -= J*np.cos(angle)
    return ene

def all_angles(my_spins, bonds):
    all_deltas = []
    for bond in bonds:
        spina = my_spins[bond[0]]
        spinb = my_spins[bond[1]]
        direct_dist = abs(spina - spinb)
        all_deltas.append(min(direct_dist,twopi - direct_dist))
    return all_deltas
    

if len(sys.argv) != 2:
    sys.exit('GIMME THE DATA FROM LONGRUNS')

J = 1.0

my_data = np.load("Longruns/"+sys.argv[1])    
pi = math.pi
twopi = 2*math.pi


dummy_data = my_data[0][0]
N = len(dummy_data)
L = int(math.sqrt(N))

all_energies = []

nbr, site_dic, x_y_dic = square_neighbors(L)
all_bonds = make_bonds(N,nbr)
bonds = []
for bond in all_bonds:
    bonds.append(tuple(bond))

for data in my_data:
    config = data[0]
    all_energies.append(grid_energy(J,config,bonds))
    
plt.plot(all_energies)
plt.ylabel('Energy of the configuration')
plt.xlabel('Number of event chains [40000 l]')
plt.show()