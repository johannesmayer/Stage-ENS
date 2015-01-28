# -*- coding: utf-8 -*-
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

def mirror(delta_phi):
    psi = math.pi - (delta_phi + math.pi)%(2*math.pi)
    return psi

##########+#########+##########+#########+##########+#########+##########+#########

J = 1.0
beta = 1.0
twopi = 2*math.pi

energy_max = energy(J,math.pi)

all_collisions = []

maximal_displacement = 10*twopi
n_times = 10**0


############+############+############+############+############+############+
"""
Since one always turns ccw one will sometimes have an initial move which will 
go into the unfavourable direction of the potential. After that move the lifted 
spin will always move in the energetically more favourable direction until it 
passes by the other spin and will continue turning until the metropolis would
reject it.
"""
############+############+############+############+############+############+

##################### DO ALL THE EVENT CHAINS VERY OFTEN #####################

for index in range(n_times):
    
    if index % 1000 == 0:
        print("PROGRESS: "+str(index)+"/"+str(n_times))
    
#+++++++++++++initialize the two spins at a random positions +++++++++++++++#
    
    angles = [random.uniform(0,twopi),random.uniform(0,twopi)]
    lift = random.choice([0,1])
    
    total_displacement = 0.0
    these_collisions = []
    these_collisions.append(angles[:])
#+++++++++++++now take care of the the angles and the displacement +++++++++++++++#
    
    
    
#+++++ GIVE THE TWO SPINS AN ENERGY ACCORDING TO PETERS PAPER ++++++#
        
################################################################################
####### SET YOUR MAXIMAL DISPLACEMENT ANGLE AND START MOVING THE SPINS #########
################################################################################
    
    while total_displacement < maximal_displacement:
        delta_phi = angles[0] - angles[1]
        upsilon = random.uniform(0.,1.)
        random_energy = -(1/beta)*math.log(upsilon)
        
#+++ TEST HOW OFTEN THEY CAN CROSS THE COMPLETE POTENTIAL WITH THAT ENERGY AND STORE REST +++#
    
        valley_crossing_number = random_energy // (2*J)
        rest_energy = random_energy % (2*J)
            
        if delta_phi < 0:
            delta_phi = delta_phi % twopi
            
###########################################################################   
#### IF YOU MOVE PHI1 THEN FOR NEGATIVE ∆PHI MOVE LEFT IN THE POTENTIAL ###
###########################################################################
        
            if lift == 0: 
                phi_bullet = 0
                phi_star = 0
                
                if delta_phi < math.pi and delta_phi > 0:
                    phi_bullet = delta_phi
                    phi_star = math.acos(1-rest_energy/J)  
                    
                else:
                    if energy_max-energy(J,delta_phi) > rest_energy:
                        #first mirror the delta phi onto its correct value between zero and pi so one can "walk up the hill to the right"
                        delta_phi = mirror(delta_phi)
                        phi_star = math.acos(math.cos(delta_phi) - rest_energy/J) - delta_phi
                    else:             
                        phi_star = delta_phi + math.acos(1-(rest_energy - energy_max + energy(J,delta_phi))/J)
                
                displacement = 0.0
                if total_displacement + phi_bullet + phi_star + valley_crossing_number*twopi < maximal_displacement :
                    displacement = phi_bullet + phi_star + valley_crossing_number*twopi
                     
                else:
                    displacement = (maximal_displacement - total_displacement) 
                                
                total_displacement += displacement   
                angles[lift] = (angles[lift] + displacement)%twopi 
                lift = (lift+1)%2  
                these_collisions.append(angles[:])
                
############################################################################
#### IF YOU MOVE PHI2 THEN FOR NEGATIVE ∆PHI MOVE RIGHT IN THE POTENTIAL ### 
############################################################################ 
                                            
            elif lift == 1:
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
                        phi_star = delta_phi + math.pi + math.acos(1-(rest_energy - energy_max + energy(J,delta_phi))/J)
                
                displacement = 0.0
                if total_displacement + phi_bullet + phi_star + valley_crossing_number*twopi < maximal_displacement :
                    displacement = phi_bullet + phi_star + valley_crossing_number*twopi
                     
                else:
                    displacement = (maximal_displacement - total_displacement) 
                
                total_displacement += displacement   
                angles[lift] = (angles[lift] + displacement)%twopi 
                lift = (lift+1)%2  
                these_collisions.append(angles[:])
                
                
                
            
#####################################################################
###+++FOR POSITIVE ∆PHI IT IS JUST THE EXACT OTHER WAY AROUND +++###
####################################################################
        elif delta_phi > 0:
            delta_phi = delta_phi % twopi
            if lift == 0:
                phi_bullet = 0
                phi_star = 0
                
                if delta_phi > math.pi and delta_phi < twopi:
                    phi_bullet = twopi - delta_phi
                    phi_star = math.acos(1-rest_energy/J)  
                    
                else:
                    if energy_max-energy(J,delta_phi) > rest_energy:
                        phi_star = math.acos(math.cos(delta_phi) - rest_energy/J) - delta_phi
                    else:             
                        phi_star = delta_phi + math.pi + math.acos(1-(rest_energy - energy_max + energy(J,delta_phi))/J)
                
                displacement = 0.0
                if total_displacement + phi_bullet + phi_star + valley_crossing_number*twopi < maximal_displacement :
                    displacement = phi_bullet + phi_star + valley_crossing_number*twopi
                     
                else:
                    displacement = (maximal_displacement - total_displacement) 
                total_displacement += displacement   
                angles[lift] = (angles[lift] + displacement)%twopi 
                lift = (lift+1)%2  
                these_collisions.append(angles[:])
                
            elif lift == 1:
                phi_bullet = 0
                phi_star = 0
                
                if delta_phi < math.pi and delta_phi > 0:
                    phi_bullet = delta_phi
                    phi_star = math.acos(1-rest_energy/J)  
                    
                else:
                    if energy_max-energy(J,delta_phi) > rest_energy:
                        delta_phi = mirror(delta_phi)
                        phi_star = math.acos(math.cos(delta_phi) - rest_energy/J) - delta_phi
                    else:             
                        phi_star = delta_phi + math.acos(1-(rest_energy - energy_max + energy(J,delta_phi))/J)
                        
                displacement = 0.0
                if total_displacement + phi_bullet + phi_star + valley_crossing_number*twopi < maximal_displacement :
                    displacement = phi_bullet + phi_star + valley_crossing_number*twopi
                     
                else:
                    displacement = (maximal_displacement - total_displacement) 
                
                total_displacement += displacement   
                angles[lift] = (angles[lift] + displacement)%twopi 
                lift = (lift+1)%2  
                these_collisions.append(angles[:])

    all_collisions.append(these_collisions[:])            
numpy.save("2 Particle Data/two_spins.npy",all_collisions)
#numpy.save("two_spins.npy",all_collisions)
print("DURATION: "+str(time.time()-starting_time)+" SECONDS")