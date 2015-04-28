import numpy, time
cimport numpy


from libc.math cimport exp, sqrt

cpdef numpy.ndarray[double, ndim = 1] random_uniform_on_sphere(numpy.int64_t dim):
    cdef double sigma = 1/sqrt(dim)
    cdef numpy.ndarray[double, ndim = 1] unit_vec
    unit_vec = numpy.array([numpy.random.normal(0,sigma) for index in xrange(dim)])
    unit_vec = unit_vec / sqrt(numpy.dot(unit_vec,unit_vec))
    return unit_vec 

cpdef numpy.ndarray[double, ndim = 1] cluster_update( numpy.int64_t N , double J, double beta, numpy.ndarray[double, ndim=2] spins, numpy.ndarray[double, ndim=1] unit_vector , numpy.ndarray[numpy.int64_t, ndim = 2] nbr):
    
    cdef numpy.int64_t size = N
    cdef numpy.int64_t starting_point = numpy.random.randint(0 , N)
    cdef numpy.ndarray[double, ndim = 1] projections = numpy.array([numpy.dot(spin,unit_vector) for spin in spins])
    cdef numpy.ndarray[numpy.int64_t, ndim = 1] pocket = numpy.array([starting_point])
    cdef numpy.ndarray[numpy.int64_t, ndim = 1] cluster = numpy.array([starting_point])
    cdef numpy.int64_t N_cluster = 1
    spins[starting_point] = spins[starting_point] - 2*projections[starting_point]*unit_vector 
    while numpy.shape(pocket)[0] != 0:
        k = pocket[0]
        pocket = numpy.delete(pocket,0)
        for neigh in nbr[k]:
            if numpy.random.uniform(0.,1.) < (1 - exp(min(0,-2*beta*J*projections[k]*projections[neigh]))):
                if neigh not in cluster:
                    pocket = numpy.append(pocket, neigh)
                    cluster = numpy.append(cluster, neigh)
                    N_cluster += 1
                    spins[neigh] = spins[neigh] - 2*projections[neigh]*unit_vector
        if N_cluster == len(spins):
            break
    return spins
    
cpdef double suscepts(numpy.int64_t N ,numpy.ndarray[double, ndim = 2] spin_config):
    cdef double mag = numpy.sum(spin_config)
    cdef double sus = numpy.dot(mag, mag)
    return sus/N