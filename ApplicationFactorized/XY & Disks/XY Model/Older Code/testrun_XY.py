# -*- coding: utf-8 -*-
#2 spin XY model subroutine
#author: JM
import numpy, random, math, time

starting_time = time.time()
##########+#########+##########+#########+##########+#########+##########+#########
"""
Two spins who can turn continuously on two neighboring sites.
The two spins turn exclusively counterclockwise alternatingly
Their interaction potential is given by E(phi_1,phi_2) = - J*Cos[phi_1-phi_2]
This program calculates the angles for phi_1 and phi_2 when they would be rejected
by the Metropolis algorithm and saves this collision point for each of the two
spins.
Here set J = 1 but it could also be taken as a 1/r distance dependent prefactor
"""
##########+#########+##########+#########+##########+#########+##########+#########
##################+ DEFINE ALL FUNCTIONS NEEDED IN THIS SECTION +##################

def energy(J,x):
    ene = -J*math.cos(x)
    return ene
    
#THIS FUNCTION MIRRORS A NUMBER BETWEEN 0 AND PI AT THE PI AXIS AND VICE VERSA

def mirror(delta_phi):
    psi = math.pi - (delta_phi + math.pi)%(2*math.pi)
    return psi

##########+#########+##########+#########+##########+#########+##########+#########

J = 1.0
beta = 1.0
twopi = 2*math.pi

energy_max = energy(J,math.pi)

all_collisions = []

chain_length = 5*math.pi
#maximal_displacement = 1.2
n_times = 10**4
#n_times = 

############+############+############+############+############+############+
"""
Since one always turns ccw one will sometimes have an initial move which will 
go into the unfavourable direction of the potential. After that move the lifted 
spin will always move in the energetically more favourable direction until it 
passes by the other spin and will continue turning until the metropolis would
reject it.
"""
############+############+############+############+############+############+
#+++++++++++++initialize the two spins at a random positions +++++++++++++++#

angles = [random.uniform(0,twopi),random.uniform(0,twopi)]
#angles = [0,0.5*math.pi]
testindex = 0


all_quantities = []

##################### DO ALL THE EVENT CHAINS VERY OFTEN #####################


for index in xrange(n_times):
    
    if index % 1000 == 0 and index != 0:
        print("PROGRESS: "+str(index)+"/"+str(n_times))
            
    lift = random.choice([0,1])
    #lift = 1    
    #angles = [0.1,1.4]
    #lift = 1
    
    total_displacement = 0.0
    these_collisions = []
    these_collisions.append(tuple([angles[:],0]))
#+++++++++++++now take care of the the angles and the displacement +++++++++++++++#
    
    
#+++++ GIVE THE TWO SPINS AN ENERGY ACCORDING TO PETERS PAPER ++++++#
        
################################################################################
####### SET YOUR MAXIMAL DISPLACEMENT ANGLE AND START MOVING THE SPINS #########
################################################################################
    
    while total_displacement < chain_length:
    
        delta_phi = angles[0] - angles[1]
        upsilon = random.uniform(0.,1.)
        while upsilon == 0:
            upsilon = random.uniform(0.,1.)
        random_energy = -(1/beta)*math.log(upsilon)
        #random_energy = 1.1*J
        valley_crossing_number = random_energy // (2*J)
        rest_energy = random_energy % (2*J)
        
        all_quantities.append(tuple([lift,delta_phi,[random_energy,rest_energy]]))
        #random_energy = 0
#+++ TEST HOW OFTEN THEY CAN CROSS THE COMPLETE POTENTIAL WITH THAT ENERGY AND STORE REST +++#
    
        

###+###+###+###+###+###+###+###+###+###+###+###+###+###+###+###+###+###+###+       
#If you move phi_0 the one needs to go in the potential given by the fixed phi_1
#to the right in order to be physically correct!
#Then depending of the position in the potential one has to overcome the summit 
#or not.
#if one moves phi_1 one has to go to the right              
###+###+###+###+###+###+###+###+###+###+###+###+###+###+###+###+###+###+###

                       
        if lift == 0:
            delta_phi = delta_phi % twopi
            phi_bullet = 0
            phi_star = 0
            
            if delta_phi > math.pi and delta_phi < twopi:
                #go down into the valley and see how far up you come
                phi_bullet = twopi - delta_phi
                phi_star = math.acos(1-rest_energy/J)  
            
            else:
                if energy_max-energy(J,delta_phi) > rest_energy:
                    phi_star = math.acos(math.cos(delta_phi) - rest_energy/J) - delta_phi
   	        else:             
                    phi_star = twopi - delta_phi + math.acos(1-(rest_energy - energy_max + energy(J,delta_phi))/J)
                
            displacement = 0.0
            if total_displacement + phi_bullet + phi_star + valley_crossing_number*twopi < chain_length :
                displacement = phi_bullet + phi_star + valley_crossing_number*twopi
                        
            else:
                displacement = (chain_length - total_displacement) 
            
                    
            while valley_crossing_number*twopi > (chain_length-total_displacement):
                valley_crossing_number = valley_crossing_number - 1                
                                                                            
            total_displacement += displacement   
            all_quantities.append(displacement)
            angles[lift] = (angles[lift] + displacement)%twopi 
            lift = (lift+1)%2  
            # save the angles and the number how often the lifted spin had to turn a full circle 
            # in order to arrive at its position (because this information is lost by taking 
            # modulo two pi
            # make sure that if one would go around too often and violate the chain length one 
            # needs to save a different number of times one actually went in a circle
             
                
            these_collisions.append(tuple([angles[:],valley_crossing_number]))
            
            if valley_crossing_number > 2:
                testindex += 1
               	
            	
            
        elif lift == 1:  
            delta_phi = delta_phi % twopi
            phi_bullet = 0
            phi_star = 0
                
            if delta_phi < math.pi and delta_phi > 0:
                phi_bullet = delta_phi
    	        phi_star = math.acos(1-rest_energy/J)  
        	        
            else:
            #first mirror the delta phi onto its correct value between zero and pi so one can "walk up the hill to the right"
                delta_phi = mirror(delta_phi)
                if energy_max-energy(J,delta_phi) > rest_energy:                    
                    phi_star = math.acos(math.cos(delta_phi) - rest_energy/J) - delta_phi
                else:             
                    phi_star = twopi - delta_phi + math.acos(1-(rest_energy - energy_max + energy(J,delta_phi))/J)
            
            displacement = 0.0
            if total_displacement + phi_bullet + phi_star + valley_crossing_number*twopi < chain_length :
                displacement = phi_bullet + phi_star + valley_crossing_number*twopi
                 
            else:
                displacement = (chain_length - total_displacement) 
            
            while valley_crossing_number*twopi > (chain_length-total_displacement):
                valley_crossing_number = valley_crossing_number - 1   
                                            
            total_displacement += displacement   
            all_quantities.append(displacement)
            angles[lift] = (angles[lift] + displacement)%twopi 
            lift = (lift+1)%2
            
                
            these_collisions.append(tuple([angles[:],valley_crossing_number]))
            
            if valley_crossing_number > 2:
                testindex += 1
               
    all_collisions.append(these_collisions[:])   
print("QUOTE: "+str(testindex/float(n_times)))
#print all_collisions
numpy.save("2 Particle Data/two_spins.npy",all_collisions)

print("DURATION: "+str(time.time()-starting_time)+" SECONDS")