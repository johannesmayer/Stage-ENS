# Wolff Cluster Algorithm for xy model in 2dimensions
# author: jm
# date: 19.02


import numpy, time, sys, os, matplotlib.pylab as plt
from cluster_functions import random_uniform_on_sphere as random_uniform_on_sphere
from cluster_functions import cluster_update as cluster_update
from cluster_functions import suscepts as suscepts


starting_time = time.time()


#************************************************************************************

def square_neighbors(L):
    N = L*L
    site_dic = {}
    x_y_dic = {}
    for j in range(N):
        row = j // L 
        column = j - row * L 
        site_dic[(row,column)] = j
        x_y_dic[j] = (row, column)
    nbr = []
    for j in range(N):
        row, column = x_y_dic[j]
        #das sind jetzt die pbc
        right_nbr = site_dic[row,(column+1)%L]
        left_nbr = site_dic[row,(column-1+L)%L]
        up_nbr = site_dic[(row+1)%L,column]
        down_nbr = site_dic[(row-1+L)%L,column]
        nbr.append((right_nbr,up_nbr,left_nbr,down_nbr))
    nbr = tuple(nbr)
    #rueckgabe sind ein tupel mit nachbarn und zwei dictionaries
    return nbr, site_dic, x_y_dic
    
#************************************************************************************

# here the dimension is the n in O(n) , the degree of symmetry
dim = 2
numpy.random.seed(1)

if len(sys.argv) != 5:
    sys.exit("GIVE ME INPUT IN FORM: L :J : BETA: NUMBER OF CLUSTER UPDATES")

L = int(sys.argv[1])
N = L*L

J = float(sys.argv[2])
beta = float(sys.argv[3])
N_cluster_updates = int(sys.argv[4])

ID = 'cluster_suscepts_L_%i_beta_%f_' %(L,beta)
outdir = 'Cluster_Data'
if not os.path.isdir(outdir):
    os.makedirs(outdir)

filename = outdir+'/'+ID

nbr, site_dic, x_y_dic = square_neighbors(L)
nbr = numpy.array(nbr)

all_suscepts = numpy.array([])
cluster_sizes = numpy.array([])
#initialize the spins 
spins =numpy.array([random_uniform_on_sphere(dim) for index in xrange(N)])

print spins

for dummy_index in xrange(N_cluster_updates):
    
    if dummy_index % (float(N_cluster_updates)/100) == 0:
        print dummy_index/float(N_cluster_updates)* 100 ,'%'
    #pick a random unit vector to project on
    unit_vec = random_uniform_on_sphere(dim)
    spins = cluster_update(N, J, beta, spins,unit_vec, nbr)
    all_suscepts = numpy.append(all_suscepts,suscepts(N,spins))
    
numpy.save(filename, all_suscepts)
print 80 * "*"
print("DURATION: "+str(time.time()-starting_time))

print all_suscepts

plt.plot(all_suscepts)
plt.show()