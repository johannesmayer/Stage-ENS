import numpy, random, time, math,matplotlib.pyplot as plt, sys

time_start = time.time()


def energy(x,phi2):
    return ((x**2)-math.cos(phi2))

factorized = True
  
twopi = 2*math.pi  

position = random.uniform(-2,2)
angle = random.uniform(0,twopi)

energies = []

N_steps = 10**6
space_step = 0.05
angle_step = twopi/20
beta = 1.0

distances = []
acceptance_index = 1

for index in range(N_steps):
    if index % 10000 == 0:
        print index
    if acceptance_index % 10000 == 0 and index != 0:
        print ("Positions: " + str(position))
        print ("Angles: "+ str(angle))
        print ("Acceptanceratio :"+str(float(acceptance_index)/float(index)))
    r_step = random.choice([-space_step,space_step])
    phi_step = random.choice([-angle_step,angle_step])
    delta_e_r = energy(position+r_step,angle)
    delta_e_phi = energy(position,angle+phi_step)
    delta_e_total = delta_e_r + delta_e_phi
    metrop = min(1,math.exp(-beta*delta_e_total))
    if factorized == True:
        metrop = min(1,math.exp(-beta*delta_e_r))*min(1,math.exp(-beta*delta_e_phi))
    if random.uniform(0.,1.) < metrop:
        acceptance_index += 1
        position += r_step
        angle = (angle + phi_step)%twopi
        
    energies.append(energy(position,angle))
print("###########################################")
print ("Mean energy: "+str(numpy.mean(energies)))
print ("Acceptanceratio :"+str(float(acceptance_index)/float(N_steps)))  


print("Duration: "+str(time.time()-time_start))
