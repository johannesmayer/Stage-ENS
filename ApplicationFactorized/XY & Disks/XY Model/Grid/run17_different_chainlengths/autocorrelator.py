# -*- coding: utf-8 -*-
#########################################################
"""
Author: JM
Input: 
    + Folder with files of same grid size and different chain lengths
      (the files should be just one list with the values of the observable)
    + Cutoff after thermalization process
    + maximal dt to which autocorrelation is calculated
    + stepwidth between two dt (for example stepwidth = 4 -> dt = 1,5,9,13 etc)
Output: 
    + Plot of autocorrelation function for observable of different chain lengths
Remark:
    + Please adapt line 42 to the filename of the data such that the 
      legend will be implemented correctly 
"""
#########################################################
import numpy, matplotlib.pylab as plt, sys, os
#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####

def autocorrelation(my_list, delta):
    mean = numpy.mean(my_list[delta:]*my_list[:-delta])
    return mean
    
def fft_autocorr(x, N):
    s = numpy.fft.fft(x)
    C = numpy.real(numpy.fft.ifft(s * numpy.conjugate(s)))
    C /= C[0]
    return C
#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####
# give program all necessary parameters

if len(sys.argv) != 5:
    sys.exit("PLEASE GIVE INPUT IN FORM: \t FOLDER WHERE .NPY FILES ARE LOCATED \t THERMAL CUTOFF \t maximal dt to calculate \t stepwidth of dt ")

directory = sys.argv[1]
thermal_cutoff = int(sys.argv[2])
delta_max = int(sys.argv[3])
stepsize = int(sys.argv[4])

# load the files from the folder into the program

file_list = sorted([f for f in os.listdir(directory) if not f.startswith('.')])
for my_file in file_list:
    if my_file.endswith('.npy'):
        #event_configs_beta_1.1199_L_32_directions_1_snap_every_10_chains_l_10_pi.npy
        chain_length_label = my_file.split('_')[13]
        filename = directory + '/' + my_file
        observable = numpy.load(filename)[thermal_cutoff:]
        observable -= observable.mean()
        correlator = fft_autocorr(observable, 1)
        plt.plot(correlator,label = chain_length_label)    

# fix plot looks
plt.title("Observable autocorrelation")
plt.xlabel('time steps dt')
plt.ylabel('Autocorrlation')
plt.xlim(0,delta_max)
plt.legend(loc='best')
plt.yscale('log')
plt.show() 
