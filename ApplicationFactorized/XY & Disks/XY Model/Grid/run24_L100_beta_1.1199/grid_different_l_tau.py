# -*- coding: utf-8 -*-
import numpy, matplotlib.pylab as plt, sys, os

def autocorrelation(my_list, delta):
    mean = numpy.mean(my_list[delta:]*my_list[:-delta])
    return mean


if len(sys.argv) != 3:
    sys.exit("PLEASE GIVE INPUT IN FORM: FOLDER WHERE NPY FILES ARE LOCATED : THERMAL CUTOFF")

directory = sys.argv[1]
thermal_cutoff = int(sys.argv[2])

delta_max = 100
stepsize = 1

file_list = sorted([f for f in os.listdir(directory) if not f.startswith('.')])

for my_file in file_list:
    if my_file.endswith('.npy'):
        #event_configs_beta_1.1199_L_32_directions_1_snap_every_10_chains_l_10_pi.npy
        chain_length_label = my_file.split('_')[13]
        filename = directory + '/' + my_file
        data = numpy.load(filename)
        #the [1] is the file where one has not the chain ends
        if len(data) == 2:
            observable = data[1]
        else:
            observable = data
        observable = observable[thermal_cutoff:]

        print numpy.shape(observable)
        observable = numpy.array(observable)
        mean = numpy.mean(observable)
        sq_exp = numpy.mean(observable*observable)
    
        all_deltas = [0]
        correlator = [1]
    
        for delta in xrange(1,delta_max,stepsize):
            all_deltas.append(delta)
            correlator.append((autocorrelation(observable,delta)-mean**2)/(sq_exp - mean**2))
    
        plt.plot(all_deltas,correlator,label = 'l = '+chain_length_label)    





plt.title("Magnetic susceptibility autocorrelation")
plt.xlabel('time steps [cluster updates / measurements (# spins touched $\\approx$ <|c|>)]')
plt.ylabel('Autocorrlation')
plt.legend(loc='best')
plt.yscale('log')

plt.show()