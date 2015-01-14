import numpy

def autocorrelation(my_list, delta):
    mean = numpy.mean(my_list[delta:]*my_list[:-delta])
    return mean
   
   
# give the standard metropolis data to data1 and the factorized one to data2   

stand_title = ""
fact_title = ""

data1 = numpy.load("/Users/johannesmayer/GitHub/Stage-ENS/ApplicationFactorized/Simulations/Data/"+str(stand_title))
data2 = numpy.load("/Users/johannesmayer/GitHub/Stage-ENS/ApplicationFactorized/Simulations/Data/"+str(fact_title))



e_data1 = data1[0]
e_data2 = data2[0]

m_data1 = data1[1]
m_data2 = data2[1]

is_cluster = False

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


correlation_max = 2500
stepsize = 1
if is_cluster == False:
    stepsize = 10


for index in range(1,correlation_max,stepsize):
    if index % 11 == 0:
        print("Progress: "+str(index)+"/"+str(correlation_max))
        
    e_correlation_function_stand.append((autocorrelation(e_data1,index)-e_mean_stand**2 )/ (e_variance_stand - e_mean_stand**2))
    e_correlation_function_fact.append((autocorrelation(e_data2,index)-e_mean_fact**2 )/ (e_variance_fact - e_mean_fact**2))
   
    m_correlation_function_stand.append((autocorrelation(m_data1,index)-m_mean_stand**2 )/ (m_variance_stand - m_mean_stand**2))
    m_correlation_function_fact.append((autocorrelation(m_data2,index)-m_mean_fact**2 )/ (m_variance_fact - m_mean_fact**2))
    
    axis.append(index)
    
    
    

correlation_stand = [axis, e_correlation_function_stand, m_correlation_function_stand]
correlation_fact = [axis, e_correlation_function_fact, m_correlation_function_stand]

numpy.save("Data/correlation_"+stand_title,correlation_stand)
numpy.save("Data/correlation_"+fact_title,correlation_fact)
    
    
    




