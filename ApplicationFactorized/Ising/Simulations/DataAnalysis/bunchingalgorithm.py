import numpy, math, random, time


N_bunches = 2
data = numpy.load("/Users/johannesmayer/GitHub/Stage-ENS/ApplicationFactorized/Simulations/Data/factorized_cluster_energies_beta_0_5.npy")
data = list(data)
data_errors = []


def bunch(liste):
    old_list = liste[:]
    new_list = []
    while old_list != []:
        ele1 = old_list.pop()   
        ele2 = old_list.pop()
        new_list.append((ele1+ele2)/2)
    old_list = new_list[:]
    return old_list    

    
for index in range(N_bunches):
    data = bunch(data)
    data_errors.append(numpy.std(data)/math.sqrt(len(data)))
    
numpy.save("factorized_cluster_bunch.npy",data_errors)