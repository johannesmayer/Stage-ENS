# -*- coding: utf-8 -*-
#2 spin XY model subroutine
#author: JM
#Date:  2015/02/23
import numpy, random, math, time, sys, cmath, os, matplotlib.pylab as plt

##################+ DEFINE ALL FUNCTIONS NEEDED IN THIS SECTION +##################
def energy(J,x):
    ene = -J*math.cos(x)
    return ene
    

def square_neighbors(L):
   N = L*L
   site_dic = {}
   x_y_dic = {}
   for j in range(N):
      row = j//L
      column = j-row*L
      site_dic[(row,column)] = j
      x_y_dic[j] = (row,column)
   nbr=[]
   for j in range(N):
      row,column = x_y_dic[j]
      right_nbr = site_dic[row,(column+1)%L]
      up_nbr = site_dic[(row+1)%L,column]
      left_nbr = site_dic[row,(column-1+L)%L]
      down_nbr = site_dic[(row-1+L)%L,column]
      nbr.append((right_nbr,up_nbr,left_nbr,down_nbr))
   nbr = tuple(nbr)
   return nbr,site_dic,x_y_dic

def mirror(delta_phi):
    psi = math.pi - (delta_phi + math.pi)%(2*math.pi)
    return psi

def calc_displacement(random_energy,J,delta_phi,direction):
    #if direction = +1 one turns to the left, if = -1 one turns all spins to the right
    
    del_phi = delta_phi % twopi
    valley_crossing_number = random_energy // (2*J)
    rest_energy = random_energy % (2*J)
    displacement = 0.0

    phi_bullet = 0
    phi_star = 0
    if direction == 1:        
        if del_phi > math.pi and del_phi < twopi:
            #go down into the valley and see how far up you come
            phi_bullet = twopi - del_phi
            phi_star = math.acos(1-rest_energy/J)  
                
        else:
            if energy_max-energy(J,del_phi) > rest_energy:
                phi_star = math.acos(math.cos(del_phi) - rest_energy/J) - del_phi
            else:             
                phi_star = twopi - del_phi + math.acos(1-(rest_energy - energy_max + energy(J,del_phi))/J)
            
    elif direction == -1:    
        if del_phi > 0 and del_phi < pi:
            #go down into the valley and see how far up you come
            phi_bullet = del_phi
            phi_star = math.acos(1-rest_energy/J)  
                
        else:
            if energy_max-energy(J,del_phi) > rest_energy:
                del_phi = mirror(del_phi)
                phi_star = math.acos(math.cos(del_phi) - rest_energy/J) - del_phi
            else:    
                phi_star = del_phi + math.acos(1-(rest_energy - energy_max + energy(J,del_phi))/J)
                
    else: 
        print('WRONG DIRECTION INPUT')
                
    displacement = phi_bullet + phi_star + valley_crossing_number*twopi
    return displacement, valley_crossing_number  
    
def xy_magnetisation(spin_config):
    N = len(spin_config)
    if type(spin_config) != numpy.ndarray:
        spin_config = numpy.array(spin_config)
    mag = sum(numpy.exp(1j*spin_config))
    return mag/float(N)
    
      
##########+#########+##########+#########+##########+#########+##########+#########

if len(sys.argv) != 5 :
    sys.exit("GIVE ME THE INPUT IN THE FORM: DIRECTORY WITH THERMALIZED CONFIGURATION : L : BETA  : SAMPLING DISTANCE ")

directory = sys.argv[1]
L = int(sys.argv[2])
J = 1.0
beta = float(sys.argv[3])
sampling_distance = float(sys.argv[4])


pi = math.pi
twopi = 2*math.pi



#make a logfile in order to write stuff in it

poss_directions = [1]


guessed_equilibration_time = 0
snap_every_n_chain = 1

outdir = "Grid_Data"
last_config_outdir = "last_config"
if not os.path.isdir(outdir):
    os.makedirs(outdir)
    
if not os.path.isdir(last_config_outdir):
    os.makedirs(last_config_outdir)

directory = sys.argv[1]

file_list = [f for f in os.listdir(directory) if not f.startswith('.') and not f.startswith('cluster')]
number_of_plots = len(file_list)


N = L*L

if len(file_list) == 0:
    spin = [random.uniform(0,2*math.pi) for k in range(N)]
else:
    spins = numpy.load(directory+'/'+file_list[0])


nbr, site_dic, x_y_dic = square_neighbors(L)
energy_max = energy(J,math.pi)
resample_after = sampling_distance * math.pi


diff_moved_spins = set()
all_moved_spins = []

overall_steps = []
different_steps = []

starting_time = time.clock()

chain_length = 100*1000*pi
#add 0.5 to make the interger not too small!
n_times = 1
    
snap_every_n_chain = int( float(resample_after) / chain_length)
if snap_every_n_chain == 0:
    snap_every_n_chain = 1
    
    
ID = 'event_configs_beta_%.4f_L_%i_directions_%i_snap_every_%i_chains_l_%i_pi' %(beta,L, sum(poss_directions),snap_every_n_chain,chain_length/pi+0.5)
filename = outdir + '/'+ ID +'.npy'
last_configuration_file = last_config_outdir+'/'+ID+'_last_config.npy'

logfile = open('log_%s.txt' %ID,'w')
logfile.write('Start with event chain run L %i and beta = %f' %(L,beta))
logfile.write('Number of event chains: %i with length %f pi \n '% (n_times, chain_length/math.pi))
logfile.write('sample at the end of each chain and also at a distance of %f' %sampling_distance)
logfile.flush()

all_inbetween_suscepts=[]
all_end_suscepts = []
global_displacement = 0.0
threshold_counter = 1.0
printing_counter = 1.0

for ith_chain in xrange(n_times):

                    
    #resample the lifting variable and then move spins throught lattice
    total_displacement = 0.0
    lift = random.randrange(N)
    direction = random.choice(poss_directions)
    #the first point in each chain is the starting point+who will move next
        
    while total_displacement < chain_length:
        
        diff_moved_spins.add(lift)
        all_moved_spins.append(lift)                        
        if global_displacement > 10*pi*printing_counter:
            percentage = 100 * (global_displacement/chain_length)
            logfile.write('# different spins moved %i \n' %len(diff_moved_spins))
            logfile.write('# spins moved %i \n' %len(all_moved_spins))
            logfile.write('%3i %% done - %9.1f seconds \n' % (percentage, time.clock() - starting_time))
            logfile.flush()
            print '# different spins moved ', len(diff_moved_spins) 
            print '# spins moved ' , len(all_moved_spins)
            print
            overall_steps.append(len(all_moved_spins))
            different_steps.append(len(diff_moved_spins))

            
            
            printing_counter += 1
            if len(diff_moved_spins) == N :
                break
            
        # give a random energy to the lifting spin
        #check with whom he will be interacting
        neigh_deltas = [(spins[lift] - spins[nbr[lift][k]])%twopi for k in range(4)]
        distance_comparison = []
        energy_vault = []
            
        for number in neigh_deltas:
            #important to sample each neighbor individually
            upsilon=random.uniform(0.,1.)
            random_energy = (-1/beta)*math.log(upsilon)
            distance_comparison.append(calc_displacement(random_energy,J,number,direction)[0])
            energy_vault.append(random_energy)
        
                    
        whos_next = nbr[lift][numpy.argmin(distance_comparison)]
        delta_phi = neigh_deltas[numpy.argmin(distance_comparison)]
        used_energy = energy_vault[numpy.argmin(distance_comparison)]
            
        rest_displacement, n_turns = calc_displacement(used_energy, J, delta_phi,direction)  
        displacement = n_turns*twopi + rest_displacement
        
        ## in this block one samples all the points one wants to see
        ######+######+######+  ######+######+######+  ######+######+######+  ######+######+######+  ######+######+######+  
        
        temp_global_displacement = global_displacement
        use_to_sample_displacement = displacement
        while temp_global_displacement + displacement > threshold_counter * resample_after and temp_global_displacement < (ith_chain+1)*chain_length:
            rest_to_displace = use_to_sample_displacement - ( threshold_counter * resample_after - temp_global_displacement )
            use_to_sample_displacement = threshold_counter * resample_after - temp_global_displacement 
            use_to_sample_spins = spins[:]
            use_to_sample_spins[lift] = (use_to_sample_spins[lift] + direction*use_to_sample_displacement)%twopi
            all_inbetween_suscepts.append(float(N)*abs(xy_magnetisation(use_to_sample_spins[:]))**2)
            threshold_counter += 1  
            temp_global_displacement += use_to_sample_displacement
            use_to_sample_displacement = rest_to_displace
        
        ######+######+######+  ######+######+######+  ######+######+######+  ######+######+######+  ######+######+######+      
            
        # see if displacement will exceed chain length and if yes truncate
        if displacement + total_displacement < chain_length:
            spins[lift] = (spins[lift]+ direction * displacement)%twopi
        else:
            displacement = chain_length - total_displacement
            spins[lift] = (spins[lift]+ direction * displacement)%twopi  
            #here append the susceptibility to its array
            if ith_chain >= guessed_equilibration_time and ith_chain % snap_every_n_chain == 0:
                all_end_suscepts.append(float(N) * abs(xy_magnetisation(spins[:])) ** 2)
                
        
        total_displacement += displacement
        global_displacement += displacement
        lift = whos_next

    if (10 * ith_chain ) % n_times == 0:
        numpy.save(filename,(all_end_suscepts,all_inbetween_suscepts))
        numpy.save(last_configuration_file,spins)
        logfile.write(80 * '*' + '\n')
        logfile.write('just saved last configuration \n')
        logfile.write('just saved the data after %i percent \n' %(100*ith_chain/float(n_times)))
        logfile.write(80 * '*' + '\n')
    

plt.plot(overall_steps, different_steps)
plt.xlabel('made moves')
plt.ylabel('number of diffrent spins involved')
plt.show()

logfile.write('Simulation is over!\n')
logfile.write('Total runtime of simulation: %f \n' % (time.clock()-starting_time))
#numpy.save(last_configuration_file,spins)
logfile.write('saved the last configuration \n')
#numpy.save(filename,(all_end_suscepts,all_inbetween_suscepts))
logfile.write('The data has the size:( %i , %i ) \n' %(len(all_end_suscepts),len(all_inbetween_suscepts)))
logfile.write('File is saved in the form (suscepts at end of every %i th chain, suscepts every %f pi), thank you for traveling with us'%(snap_every_n_chain,sampling_distance))
logfile.close()
    
