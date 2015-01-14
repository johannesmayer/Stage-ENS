import numpy

def autocorrelation(my_list, delta):
    mean = numpy.mean(my_list[delta:]*my_list[:-delta])
    return mean
   
   
# give the standard metropolis data to data1 and the factorized one to data2   
"""
data1 = numpy.load("/Users/johannesmayer/GitHub/Stage-ENS/ApplicationFactorized/Simulations/energies_local_stand_beta_0_5.npy")
data2 = numpy.load("/Users/johannesmayer/GitHub/Stage-ENS/ApplicationFactorized/Simulations/energies_local_fact_beta_0_5.npy")
"""

data1 = numpy.load("/Users/johannesmayer/GitHub/Stage-ENS/ApplicationFactorized/Simulations/energies_local_stand_beta_crit.npy")
data2 = numpy.load("/Users/johannesmayer/GitHub/Stage-ENS/ApplicationFactorized/Simulations/energies_local_fact_beta_crit.npy")


is_cluster = False

axis = []
correlation_function_stand = []
correlation_function_fact = []
mean_stand = numpy.mean(data1)
mean_fact = numpy.mean(data2)

variance_stand = numpy.mean(data1*data1)
variance_fact = numpy.mean(data2*data2)


correlation_max = 2500
stepsize = 1
if is_cluster == False:
    stepsize = 10


for index in range(1,correlation_max,stepsize):
    if index % 11 == 0:
        print("Progress: "+str(index)+"/"+str(correlation_max))
    correlation_function_stand.append((autocorrelation(data1,index)-mean_stand**2 )/ (variance_stand - mean_stand**2))
    correlation_function_fact.append((autocorrelation(data2,index)-mean_fact**2 )/ (variance_fact - mean_fact**2))
    axis.append(index)

correlation_stand = [axis, correlation_function_stand]
correlation_fact = [axis, correlation_function_fact]


numpy.save("correlation_stand_metrop_beta_crit.npy",correlation_stand)
numpy.save("correlation_fact_metrop_beta_crit.npy",correlation_fact)

"""
numpy.save("correlation_stand_cluster_beta_crit.npy",correlation_stand)
numpy.save("correlation_fact_cluster_beta_crit.npy",correlation_fact)
"""






