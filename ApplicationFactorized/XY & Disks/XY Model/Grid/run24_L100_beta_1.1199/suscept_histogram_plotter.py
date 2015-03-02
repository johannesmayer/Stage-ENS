# -*- coding: utf-8 -*-
import numpy, matplotlib.pylab as plt, sys, os

if len(sys.argv) != 3:
    sys.exit("PLEASE GIVE INPUT IN FORM: FOLDER WHERE NPY FILES ARE LOCATED : THERMAL CUTOFF")

directory = sys.argv[1]

labels = ['ends','inbetween']

j = 0

file_list = [f for f in os.listdir(directory) if not f.startswith('.') and not f.startswith('cluster')]
number_of_plots = len(file_list)

fig, ax = plt.subplots(1,number_of_plots, figsize = (14,6))

temp_binning = []
make_binning = 1


for my_file in file_list:
    if my_file.endswith('.npy'):
        chain_length_label = my_file.split('_')[13]
        filename = directory + '/' + my_file
        data = numpy.load(filename)
        for index in xrange(len(data)):
            measurements = data[index]
            if make_binning:
                temp_binning = 100
            temp_histo, binning = numpy.histogram(measurements, bins = temp_binning, normed = True)    
            temp_binning = binning
            make_binning = ( make_binning +1 ) % 2   
            bin_centres = 0.5 * (binning[1:] + binning[:-1])
            temp_histo = numpy.cumsum(temp_histo)*(binning[1] - binning[0])
            label = labels[index]
            ax[j].plot(bin_centres,temp_histo, label = label)
        ax[j].set_ylim([0,1.01]) 
        ax[j].set_title(chain_length_label)   
        ax[j].legend(loc = 'upper left')
        plt.legend(loc = 'upper left')
        j += 1

"""

plt.title("Magnetic susceptibility histogram")
plt.xlabel('Magnetic susceptibility')
plt.ylabel('Frequency')

"""
#plt.tight_layout()
plt.show()