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
    + lower boundary of fit
    + higher boundary of fit
Output: 
    + Plot of autocorrelation function for observable of different chain lengths
    + Plot of fitted curves into the plot iwth autocorrelators
Remark:
    + Please adapt line 42 to the filename of the data such that the 
      legend will be implemented correctly 
"""
#########################################################
import numpy, matplotlib.pylab as plt, sys, os
import matplotlib.cm as cm
#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####

def autocorrelation(my_list, delta):
    mean = numpy.mean(my_list[delta:]*my_list[:-delta])
    return mean

#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####
# give program all necessary parameters

if len(sys.argv) != 7:
    sys.exit("PLEASE GIVE INPUT IN FORM: : FOLDER WHERE .NPY FILES ARE LOCATED : THERMAL CUTOFF : maximal dt to calculate : stepwidth of dt : fit from : fit to ")

directory = sys.argv[1]
thermal_cutoff = int(sys.argv[2])
delta_max = int(sys.argv[3])
stepsize = int(sys.argv[4])
dt_min_fit = int(sys.argv[5])
dt_max_fit = int(sys.argv[6])

outdir = 'stored_autocorrelators'

if not os.path.isdir(outdir):
    os.makedirs(outdir)
    
# load the files from the folder into the program

file_list = sorted([f for f in os.listdir(directory) if not f.startswith('.')])
colormap = iter(cm.rainbow(numpy.linspace(0,1,len(file_list))))

for my_file in file_list:
    if my_file.endswith('.npy'):
        #event_configs_beta_1.1199_L_32_directions_1_snap_every_10_chains_l_10_pi.npy
        chain_length_label = my_file.split('_')[13]
        filename = directory + '/' + my_file
        outfile = outdir + '/' + 'autocorr_' + my_file
        observable = numpy.load(filename)[thermal_cutoff:]
        observable = numpy.array(observable)
        mean = numpy.mean(observable)
        sq_exp = numpy.mean(observable*observable)
    
        all_deltas = [0]
        correlator = [1]
    
        for delta in xrange(1,delta_max,stepsize):
            print 'l', chain_length_label, delta, delta_max
            all_deltas.append(delta)
            correlator.append((autocorrelation(observable,delta)-mean**2)/(sq_exp - mean**2)) 
        safile = (all_deltas, correlator)
        numpy.save(outfile, safile)
        
        # HERE THE FIT IS DONE OF THE LOGARITHMIC DATA######################
        tau_corr = 0.
        x = numpy.array(all_deltas[dt_min_fit:dt_max_fit+1])
        neg_log_y = -1 * numpy.log(correlator[dt_min_fit:dt_max_fit+1])
        inv_tau, coeff = numpy.polyfit(x, neg_log_y, 1)
        print inv_tau, coeff
        if inv_tau:
            tau_corr = 1.0/inv_tau
        else: tau_corr = float('inf')
        ####################################################################
        
        color = next(colormap)
        chain_length_label = 'l= '+ chain_length_label + ' $\\tau= $%f'%tau_corr
        
        plt.plot(x,numpy.exp(-coeff)*numpy.exp(-x/tau_corr), c = color, alpha = 0.7, lw = 2.)
        plt.plot(all_deltas,correlator,c = color, marker = '.',label = chain_length_label)    

        
# fix plot looks
plt.title("Observable autocorrelation")
plt.xlabel('time steps dt')
plt.ylabel('Autocorrlation')
plt.legend(loc='best')
plt.yscale('log')
plt.show()