# Wolff Cluster Algorithm for xy model in 2dimensions
# author: jm
# date: 19.02


import math, numpy, random, time, sys, os


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

    
def random_uniform_on_sphere(dim):
    sigma = 1/math.sqrt(dim)
    unit_vec = numpy.array([random.gauss(0,sigma) for index in xrange(dim)])
    unit_vec /= math.sqrt(sum(unit_vec**2))
    return unit_vec
    
def xy_magn(spin_config):
    spin_config_ = spin_config[:]
    N = len(spin_config_)
    if type(spin_config_) != numpy.ndarray:
        spin_config_ = numpy.array(spin_config_)
    mag = sum(spin_config_)
    return mag/float(N)

def cluster_update(spins, unit_vector):
    starting_point = random.randrange(N)
    projections = numpy.array([numpy.dot(spin,unit_vector) for spin in spins])
    
    pocket = [starting_point]
    cluster = [starting_point]
    N_cluster = 1
    
    spins[starting_point] = spins[starting_point] - 2*projections[starting_point]*unit_vector 
    while pocket != []:
        k = pocket.pop()
        for neigh in nbr[k]:
            if random.uniform(0.,1.) < (1 - math.exp(min(0,-2*beta*J*projections[k]*projections[neigh]))):
                if neigh not in cluster:
                    pocket.append(neigh)
                    cluster.append(neigh)
                    N_cluster += 1
                    spins[neigh] = spins[neigh] - 2*projections[neigh]*unit_vector
        if N_cluster == len(spins):
            break
    return spins, float(N_cluster)
    


#************************************************************************************

# here the dimension is the n in O(n) , the degree of symmetry
dim = 2

if len(sys.argv) != 5:
    sys.exit("GIVE ME INPUT IN FORM:\tL\tJ\tBETA\tNUMBER OF CLUSTER UPDATES")


twopi = 2*math.pi
pi = math.pi

L = int(sys.argv[1])
N = L*L

J = float(sys.argv[2])
beta = float(sys.argv[3])

N_cluster_updates = int(sys.argv[4])


nbr, site_dic, x_y_dic = square_neighbors(L)
all_suscepts = []
cluster_sizes = []
#initialize the spins 
spins =numpy.array([random_uniform_on_sphere(dim) for index in xrange(N)])
#spins = numpy.array([[1.,0.] for index in xrange(N)])

starting_time = time.clock()

outdir = "Grid_Data"
ID = 'L_' + str(L) + "_beta_" + str(beta)
filename = 'cluster_last_config_' + ID + '.npy'
filename = outdir + '/' + filename

logfile = open('log_%s.txt' % ID, 'w')
logfile.write('start run with L=%i and beta=%f\n' % (L, beta))
logfile.write('number of wolff steps: %i\n' % N_cluster_updates)

if not os.path.isdir(outdir):
    os.makedirs(outdir)

for dummy_index in xrange(N_cluster_updates):
    
    if (dummy_index * 100) % N_cluster_updates == 0 and dummy_index > 0:
        percentage = dummy_index * 100 / N_cluster_updates
        logfile.write('%3i%% done - %9.1f seconds\t' % (percentage, time.clock() - starting_time))
        numpy.save(filename, spins)
        logfile.write('saved last configuration \n')

        mean_cluster_size = numpy.mean(cluster_sizes)
        logfile.write('avg cluster size: %.6f\n' % mean_cluster_size)
        logfile.flush()

    #pick a random unit vector to project on
    unit_vec = random_uniform_on_sphere(dim)
    spins, n_cluster_members = cluster_update(spins,unit_vec)
    
    cluster_sizes.append(n_cluster_members)
    magn_pp = xy_magn(spins)


numpy.save(filename, spins)

logfile.write('%3i%% done - %9.1f seconds\n' % (100, time.clock() - starting_time))
logfile.write('end\n')
logfile.write('saving things on %s\n' % filename)
mean_cluster_size = numpy.mean(cluster_sizes)
logfile.write('average cluster size: %.6f\n' % mean_cluster_size)
logfile.write('ciao ciao\n')
logfile.close()


