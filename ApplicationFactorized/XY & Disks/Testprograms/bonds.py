import numpy, math, random, time
    
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
    bonds = numpy.unique(bonds)
    return bonds

def all_angles(my_spins, nbr):
    N = len(my_spins)
    all_delta_phi = []    
    for index in range(N):
        for neigh in nbr[index]:
            direct_dist = abs((my_spins[index]-my_spins[neigh]))
            all_delta_phi.append(min(direct_dist, twopi -direct_dist))
    all_delta_phi = numpy.unique(all_delta_phi)
    return list(all_delta_phi)

def bond_angles(my_spins, bonds):
    all_deltas = []
    for bond in bonds:
        spina = my_spins[bond[0]]
        spinb = my_spins[bond[1]]
        direct_dist = abs(spina - spinb)
        all_deltas.append(min(direct_dist,twopi - direct_dist))
    return all_deltas
    

def grid_energy(J,my_config,nbr):
    ene = 0.
    my_deltas = all_angles(my_config, nbr)
    for angle in my_deltas:
        ene -= J*numpy.cos(angle)
    return ene

def quick_energy(J,my_config,bondes):
    ene = 0.
    my_deltas = bond_angles(my_config, bondes)
    for angle in my_deltas:
        ene -= J*numpy.cos(angle)
    return ene

L = 50
N = L*L
J = 1.
twopi = 2*math.pi
pi = math.pi

nbr, site_dic, x_y_dic = square_neighbors(L)

all_bonds = make_bonds(N,nbr)
my_bonds = []
for bond in all_bonds:
    my_bonds.append(tuple(bond))



test_config = [random.uniform(0.,1.) for k in range(N)]

#print test_config
starting_time = time.time()

energy = quick_energy(J,test_config,my_bonds)

print energy



print("DURATION: "+str(time.time()-starting_time))

 
    
    
    
    
    
    
    
