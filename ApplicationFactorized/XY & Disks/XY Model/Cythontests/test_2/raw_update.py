
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
    