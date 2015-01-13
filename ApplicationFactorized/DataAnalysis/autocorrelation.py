import numpy

def autocorrelation(liste, delta):
    first_list = []
    for index in range(len(liste)-delta):
        first_list.append(liste[index]*liste[index+delta])
    mean = numpy.mean(first_list)
    return mean
    
data = numpy.load("/Users/johannesmayer/GitHub/Stage-ENS/ApplicationFactorized/Simulations/energies_local_stand_beta_0_5.npy")
data = list(data)

axis = []
correlation_function = []

correlation_max = 100

for index in range(correlation_max):
    if index % 10 == 0:
        print("Progress: "+str(index)+"/"+str(correlation_max))
    correlation_function.append(autocorrelation(data,index))
    axis.append(index)
    
correlation = [axis, correlation_function]

numpy.save("correlation_standard_metrop.npy",correlation)
