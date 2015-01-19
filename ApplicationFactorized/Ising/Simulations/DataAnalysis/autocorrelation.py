import numpy, sys


def autocorrelation(my_list, delta):
    mean = numpy.mean(my_list[delta:]*my_list[:-delta])
    return mean
   

if len(sys.argv) != 4:
    sys.exit("########### WRONG INPUT! ############ GIVE ME THE INPUT IN THE ORDER: <Cluster/Local> _ <standard-file in SimulationData> _ <factorized-file in SimulationData>")



is_cluster = sys.argv[1]
stand_title = sys.argv[2]   
fact_title = sys.argv[3]    
     
# give the standard metropolis data to data1 and the factorized one to data2   

if is_cluster == "Cluster":
    is_cluster = True
if is_cluster == "Local":
    is_cluster = False
    
#stand_title = "local_stand_beta_crit.npy"
#fact_title = "local_fact_beta_crit.npy"

data1 = numpy.load("SimulationData/"+stand_title)
data2 = numpy.load("SimulationData/"+fact_title)



e_data1 = data1[0]
e_data2 = data2[0]

m_data1 = data1[1]
m_data2 = data2[1]



axis = []

e_correlation_function_stand = []
e_correlation_function_fact = []

m_correlation_function_stand = []
m_correlation_function_fact = []

e_mean_stand = numpy.mean(e_data1)
e_mean_fact = numpy.mean(e_data2)

e_variance_stand = numpy.mean(e_data1*e_data1)
e_variance_fact = numpy.mean(e_data2*e_data2)




m_correlation_function_stand = []
m_correlation_function_fact = []

m_mean_stand = numpy.mean(m_data1)
m_mean_fact = numpy.mean(m_data2)

m_variance_stand = numpy.mean(m_data1*m_data1)
m_variance_fact = numpy.mean(m_data2*m_data2)


correlation_max = 1000
stepsize = 1
if is_cluster == False:
    stepsize = 10
    correlation_max = 10000

for index in range(1,correlation_max,stepsize):
    if index % 11 == 0:
        print("Progress: "+str(index)+"/"+str(correlation_max))
        
    e_correlation_function_stand.append((autocorrelation(e_data1,index)-e_mean_stand**2 )/ (e_variance_stand - e_mean_stand**2))
    e_correlation_function_fact.append((autocorrelation(e_data2,index)-e_mean_fact**2 )/ (e_variance_fact - e_mean_fact**2))
   
    m_correlation_function_stand.append((autocorrelation(m_data1,index)-m_mean_stand**2 )/ (m_variance_stand - m_mean_stand**2))
    m_correlation_function_fact.append((autocorrelation(m_data2,index)-m_mean_fact**2 )/ (m_variance_fact - m_mean_fact**2))
    
    axis.append(index)
 

correlation_stand = [axis, e_correlation_function_stand, m_correlation_function_stand]
correlation_fact = [axis, e_correlation_function_fact, m_correlation_function_fact]

numpy.save("AnalysisData/correlation_"+stand_title,correlation_stand)
numpy.save("AnalysisData/correlation_"+fact_title,correlation_fact)
    
    
    




