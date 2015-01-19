import numpy, sys



def autocorrelation(my_list, delta):
    mean = numpy.mean(my_list[delta:]*my_list[:-delta])
    return mean
   
   
#####################################################################################

if len(sys.argv) != 3:
    sys.exit("########### WRONG INPUT! ############ GIVE ME THE INPUT IN THE ORDER: <standard-file in SimulationData> _ <factorized-file in SimulationData>")

std_data = numpy.load("SimulationData/"+sys.argv[1])
fact_data = numpy.load("SimulationData/"+sys.argv[2])

std_flip_times = std_data[0]
fact_flip_times = fact_data[0]

std_ene = []
std_mag = []

fact_ene = []
fact_mag = []


auto_max = 2**10

step_size = 5

std_energy_autocorr = []
std_magnet_autocorr = []

fact_energy_autocorr = []
fact_magnet_autocorr = []

#creat your lists you wanna calculate the autocorr. from

for index in range(len(std_flip_times)):
    
    std_ene.extend([std_data[1][index]]*std_flip_times[index])
    std_mag.extend([std_data[2][index]]*std_flip_times[index])
    
    
for index in range(len(fact_flip_times)):    
    fact_ene.extend([fact_data[1][index]]*fact_flip_times[index])
    fact_mag.extend([fact_data[2][index]]*fact_flip_times[index])


std_ene = numpy.array(std_ene)
std_mag = numpy.array(std_mag)
fact_ene = numpy.array(fact_ene)
fact_mag = numpy.array(fact_mag)

axis = []


std_ene_mean= numpy.mean(std_ene)
fact_ene_mean = numpy.mean(fact_ene)

std_mag_mean= numpy.mean(std_mag)
fact_mag_mean = numpy.mean(fact_mag)

std_e_variance =numpy.mean(std_ene*std_ene)
fact_e_variance = numpy.mean(fact_ene*fact_ene)

std_m_variance = numpy.mean(std_mag*std_mag)
fact_m_variance = numpy.mean(fact_mag*fact_mag)


for i_sweep in range(1,auto_max,step_size):
    
    axis.append(i_sweep)    
        
    std_energy_autocorr.append((autocorrelation(std_ene,i_sweep)-std_ene_mean**2)/(std_e_variance-std_ene_mean**2))   
    std_magnet_autocorr.append((autocorrelation(std_mag,i_sweep)-std_mag_mean**2)/(std_m_variance-std_mag_mean**2))   
   
    fact_energy_autocorr.append((autocorrelation(fact_ene,i_sweep)-fact_ene_mean**2)/(fact_e_variance-fact_ene_mean**2))    
    fact_magnet_autocorr.append((autocorrelation(fact_mag,i_sweep)-fact_mag_mean**2)/(fact_m_variance-fact_mag_mean**2))    

print std_energy_autocorr

corr_stand = [axis,std_energy_autocorr,std_magnet_autocorr]
corr_fact = [axis,fact_energy_autocorr,fact_magnet_autocorr]
 
#print corr_stand
 
path_std = "AnalysisData/fttc_std_correlation_"+sys.argv[1]
path_fact = "AnalysisData/fttc_fact_correlation_"+sys.argv[2]

numpy.save(path_std,corr_stand)
numpy.save(path_fact,corr_fact)
 
print("DATA SAVED IN "+path_std)
print("DATA SAVED IN "+path_fact)
    