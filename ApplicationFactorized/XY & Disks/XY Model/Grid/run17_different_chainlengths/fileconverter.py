# little file converter to extract only the notchainend-filepart
import numpy, os, sys

if len(sys.argv) != 3:
    sys.exit('PLEASE GIVE INPUT IN FORM: \t FOLDER WITH FILES \t NAME OF OUTPUT FOLDER')
    

directory = sys.argv[1]
output_directory = sys.argv[2]

if not os.path.isdir(output_directory):
    os.makedirs(output_directory)

file_list = sorted([f for f in os.listdir(directory) if not f.startswith('.')])

for my_file in file_list:
    if my_file.endswith('.npy'):
        #event_configs_beta_1.1199_L_32_directions_1_snap_every_10_chains_l_10_pi.npy
        print my_file
        chain_length_label = my_file.split('_')[13]
        filename = directory + '/' + my_file
        output_filename = output_directory+'/'+my_file
        data = numpy.load(filename)
        if len(data) == 2:
            observable = data[1]
        else:
            observable = data
        numpy.save(output_filename,observable)