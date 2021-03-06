# -*- coding: utf-8 -*-
#2 spin XY model subroutine
#author: JM
#Date:  2015/02/03
import numpy, random, math, time, sys, cmath, os

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


def calc_displacement(random_energy,J,delta_phi):
    del_phi = delta_phi % twopi
    valley_crossing_number = random_energy // (2*J)
    rest_energy = random_energy % (2*J)
    displacement = 0.0

    phi_bullet = 0
    phi_star = 0
            
    if del_phi > math.pi and del_phi < twopi:
        #go down into the valley and see how far up you come
        phi_bullet = twopi - del_phi
        phi_star = math.acos(1-rest_energy/J)  
            
    else:
        if energy_max-energy(J,del_phi) > rest_energy:
            phi_star = math.acos(math.cos(del_phi) - rest_energy/J) - del_phi
        else:             
            phi_star = twopi - del_phi + math.acos(1-(rest_energy - energy_max + energy(J,del_phi))/J)
                
    displacement = phi_bullet + phi_star + valley_crossing_number*twopi
    return displacement, valley_crossing_number  
    
def xy_magnetisation(spin_config):
    N = len(spin_config)
    if type(spin_config) != numpy.ndarray:
        spin_config = numpy.array(spin_config)
    mag = sum(numpy.exp(1j*spin_config))
    return mag/float(N)
    
      
##########+#########+##########+#########+##########+#########+##########+#########

if len(sys.argv) != 6 :
    sys.exit("GIVE ME THE INPUT IN THE FORM: L : J : BETA : CHAINLENGHT IN UNITS OF PI : NUMBER OF CHAINS")


L = int(sys.argv[1])
J = float(sys.argv[2])
beta = float(sys.argv[3])
chain_length = float(sys.argv[4])*math.pi
n_times = int(sys.argv[5])

# make a logfile in order to write stuff in it

outdir = "Grid_Data"
ID = 'xy_grid_event_suscepts_beta_%.4f_L_%i' %(beta,L)
filename = outdir + '/'+ ID +'.npy'

if not os.path.isdir(outdir):
    os.makedirs(outdir)

logfile = open('log_%s.txt' %ID,'w')
logfile.write('Start with event chain run L %i and beta = %f \n' %(L,beta))
logfile.write('Number of event chains: %i with length %f pi \n '% (n_times, chain_length/math.pi))
logfile.flush()

N = L*L
nbr, site_dic, x_y_dic = square_neighbors(L)

energy_max = energy(J,math.pi)

pi = math.pi
twopi = 2*math.pi

all_suscepts = []
chain_moves = []

spins = [random.uniform(0,2*math.pi) for k in range(N)]

starting_time = time.clock()


for i_sweep in range(n_times):
    if (i_sweep*100) % n_times == 0 and i_sweep != 0:
        percentage = i_sweep * 100 / n_times
        logfile.write('%3i %% done - %9.1f seconds\n' % (percentage, time.clock() - starting_time))
        logfile.flush()
                    
    #resample the lifting variable and then move spins throught lattice
    total_displacement = 0.0
    lift = random.randrange(N)
    #the first point in each chain is the starting point+who will move next
    moves_this_chain = 0 

    while total_displacement < chain_length:
        moves_this_chain += 1
        # give a random energy to the lifting spin
        #check with whom he will be interacting
        neigh_deltas = [(spins[lift] - spins[nbr[lift][k]])%twopi for k in range(4)]
        distance_comparison = []
        energy_vault = []
        
        for number in neigh_deltas:
            #important to sample each neighbor individually
            upsilon=random.uniform(0.,1.)
            random_energy = (-1/beta)*math.log(upsilon)
            distance_comparison.append(calc_displacement(random_energy,J,number)[0])
            energy_vault.append(random_energy)
            
        whos_next = nbr[lift][numpy.argmin(distance_comparison)]
        delta_phi = neigh_deltas[numpy.argmin(distance_comparison)]
        used_energy = energy_vault[numpy.argmin(distance_comparison)]
        
        rest_displacement, n_turns = calc_displacement(used_energy, J, delta_phi)  
        displacement = n_turns*twopi + rest_displacement
         
        # see if displacement will exceed chain length and if yes truncate
        if displacement + total_displacement < chain_length:
            spins[lift] = (spins[lift]+displacement)%twopi
        else:
            displacement = chain_length - total_displacement
            spins[lift] = (spins[lift]+displacement)%twopi  
            #here append the susceptibility to its array
            all_suscepts.append(float(N)*abs(xy_magnetisation(spins)) ** 2)
 
        total_displacement += displacement
        lift = whos_next
    chain_moves.append(moves_this_chain)

    if (i_sweep * 10) % n_times == 0 and i_sweep != 0:
        numpy.save(filename,all_suscepts)
        logfile.write('saving %i data\n' % len(all_suscepts))

numpy.save(filename,all_suscepts)
logfile.write('saving %i data (all)\n' % len(all_suscepts))


logfile.write('Simulation is over!\n')
logfile.write('Total runtime of simulation: %f \n' % (time.clock()-starting_time))
avg_moves = numpy.mean(chain_moves)
logfile.write('Average Moves per event chain: %f \n' % avg_moves)
logfile.write('File is saved, thank you for traveling with us')
