

# -*- coding: utf-8 -*-
#2 spin XY model subroutine
#author: JM
import numpy as numpy, random, math, time, sys

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

def xy_magnetisation(spin_config):
    N = len(spin_config)
    if type(spin_config) != numpy.ndarray:
        spin_config = numpy.array(spin_config)
    mag = sum(numpy.exp(1j*spin_config))
    return mag/float(N)
    

########################+#######################+###########################+

if len(sys.argv) != 5 :
    sys.exit(" GIVE MIT INPUT IN ORDER: COUPLING J, BETA, NUMBER OF SWEEPS , MOVES PER SWEEP ")

different_sizes = [10,15,20]

    
pi = math.pi
twopi = 2*math.pi
    
J = float(sys.argv[1])
beta = float(sys.argv[2])
n_times = int(sys.argv[3])
moves_per_sweep = int(sys.argv[4])



step = 0.7*pi

print("stepsize: "+"["+str(-step)+","+str(step)+"]")

for L in different_sizes:
    
    starting_time = time.time()
    
    print("System Size of this run: "+str(L))
    N=L*L

    nbr, site_dic, x_y_dic = square_neighbors(L)
    
    
    spins = [random.uniform(0,2*pi) for k in xrange(N)]
    all_suscepts = []
    successor = 0.    
    
    SKIP_ = 1
    
    for i_sweep in xrange(n_times):
        
        if i_sweep % 1000 == 0:
            print i_sweep,n_times, 'in time of ',time.time()-starting_time, ' seconds'
            logfile = open('status.dat', 'w')
            logfile.write('%i / %i\n' % (i_sweep, n_times))
            logfile.close()
        for index in xrange(moves_per_sweep):
            who_moves = random.choice(numpy.arange(N))
            neighs = nbr[who_moves]
            moved_spin = spins[who_moves]
            move = random.uniform(-step,step)
            if random.uniform(0.,1.) < math.exp(-beta*(energy(J,moved_spin+move,neighs,spins)-energy(J,moved_spin,neighs,spins))):
                spins[who_moves] = (spins[who_moves] + move)%twopi
                successor += 1
        if i_sweep % SKIP_ == 0:
            all_suscepts.append(abs(xy_magnetisation(spins))**2)   
    logfile.close()
            
    print("SUCCESS RATE METROPOLIS: "+str(successor/n_times/moves_per_sweep))
    print("DURATION FOR THIS SIZE: "+str(time.time()-starting_time))
    print("MOVES PER SWEEP: "+str(moves_per_sweep))
    print("I am skipping %i steps before next measurement" % SKIP_)
    
    
    #numpy.save("Grid Data/xy_grid_markov_suscepts_beta_"+str(beta)+"_L_"+str(L)+".npy",all_suscepts)
