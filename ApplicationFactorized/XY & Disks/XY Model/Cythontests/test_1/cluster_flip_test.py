import numpy

from libc.math cimport exp
cimport numpy

cdef int L = 10
cdef int N = L*L

cdef numpy.ndarray[dtype = float, dim = 1] spins = numpy.array([random_uniform_on_sphere(dim) for index in xrange(N)])




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



cdef numpy.ndarray[spin_data_type, ndim = 1] cluster_update( cdef numpy.ndarray[spin_data_type ,ndim = 1] spins, cdef numpy.ndarray[spin_data_type , ndim = 1] unit_vector ):
    
    cdef int starting_point
    cdef numpy.ndarray[spin_data_type, ndim = 1 ] 
    
    cdef numpy.ndarray[int, ndim = 1] pocket 
    cdef numpy.ndarray[int, ndim = 1] cluster 
    
    cdef numpy.ndarray[int, ndim = 1] neighbors
    
    starting_point = numpy.random.randrange(N) 
     
    projections = numpy.array([numpy.dot(spin,unit_vector) for spin in spins])
    numpy.append(pocket, starting_point)
    numpy.append(cluster, starting_point)
    
    cdef int N_cluster = 1
    N_cluster = 1
    
    spins[starting_point] = spins[starting_point] - 2*projections[starting_point]*unit_vector 
    
    while len(pocket) != 0:
        k = pocket[0]
        k = numpy.delete(pocket, 0)
        neighbors = nbr[k]
        for neigh in neighbors:
            if random.uniform(0.,1.) < (1 - exp(min(0,-2*beta*J*projections[k]*projections[neigh]))):
                if neigh not in cluster:
                    numpy.append(pocket,neigh)
                    numpy.append(cluster, neigh)
                    N_cluster += 1
                    spins[neigh] = spins[neigh] - 2*projections[neigh]*unit_vector
        if N_cluster == len(spins):
            break
    return spins#, float(N_cluster)
    
    