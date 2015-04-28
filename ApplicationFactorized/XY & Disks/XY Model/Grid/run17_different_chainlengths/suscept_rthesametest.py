# -*- coding: utf-8 -*-
import numpy, matplotlib.pylab as plt, sys, os

if len(sys.argv) != 3:
    sys.exit("PLEASE GIVE INPUT IN FORM: FOLDER WHERE NPY FILES ARE LOCATED : THERMAL CUTOFF")

directory = sys.argv[1]

j = 0

file_list = [f for f in os.listdir(directory) if not f.startswith('.') and not f.startswith('cluster')]
number_of_hists = len(file_list)


temp_binning = []
make_binning = 1


for my_file in file_list:
    if my_file.endswith('.npy'):
        filename = directory + '/' + my_file
        measurements = numpy.load(filename)
        chain_length_label = my_file.split('_')[13]
        if make_binning:
            temp_binning = 100
        temp_histo, binning = numpy.histogram(measurements, bins = temp_binning, normed = True)    
        temp_binning = binning
        make_binning = ( make_binning +1 ) % 2   
        bin_centres = 0.5 * (binning[1:] + binning[:-1])
        temp_histo = numpy.cumsum(temp_histo)*(binning[1] - binning[0])
        label = chain_length_label
        plt.plot(bin_centres,temp_histo, label = label)

plt.ylim([0,1.01])   
plt.legend(loc = 'upper left')


plt.title("Cumulative Magnetic susceptibility distribution")
plt.xlabel('Magnetic susceptibility')
plt.ylabel('Integrated Frequency')



plt.show()