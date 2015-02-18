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

#constructing a square lattice and find all the bonds

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

########################+#######################+###########################+

if len(sys.argv) != 5 :
    sys.exit(" GIVE MIT INPUT IN ORDER: GRID EDGE LENGTH L , COUPLING J, BETA, NUMBER OF SWEEPS ")



L=int(sys.argv[1])
N=L*L

pi = math.pi
twopi = 2*math.pi

J = float(sys.argv[2])
beta = float(sys.argv[3])
step = 0.5*pi

nbr, site_dic, x_y_dic = square_neighbors(L)
all_bonds = make_bonds(N,nbr)
bonds = []
for bond in all_bonds:
    bonds.append(tuple(bond))


spins = [random.uniform(0,2*pi) for k in xrange(N)]
all_energies = []
successor = 0.

all_steps = []

n_times = int(sys.argv[4])

for i_sweep in xrange(n_times):
    
    if i_sweep % 1000 == 0:
        print i_sweep,n_times, 'in time of ',time.time()-starting_time, ' seconds'
    for index in xrange(N):
        who_moves = random.choice(np.arange(N))
        neighs = nbr[who_moves]
        moved_spin = spins[who_moves]
        move = random.uniform(-step,step)
        if random.uniform(0.,1.) < math.exp(-beta*(energy(J,moved_spin+move,neighs,spins)-energy(J,moved_spin,neighs,spins))):
            spins[who_moves] = (spins[who_moves] + move)%twopi
            successor += 1
            all_steps.append(abs(move))
        else: all_steps.append(0.)
    all_energies.append(grid_energy(J,spins,bonds))   
        
    #all_delta_phis.extend(all_angles(config,nbr))
print("RATE: "+str(successor/n_times/N))
print("AVERAGE DISPLACEMENT PER SWEEP: "+str(N*np.mean(all_steps)/pi)+"Pi")

print("DURATION: "+str(time.time()-starting_time))

plt.plot(all_energies)
plt.show()

np.save("Grid Data/grid_markov_energies_beta_"+str(beta)+"_L_"+str(L)+".npy",all_energies)

