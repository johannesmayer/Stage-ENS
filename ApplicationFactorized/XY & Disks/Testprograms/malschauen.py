import numpy, random, time, math,matplotlib.pyplot as plt, sys

time_start = time.time()


def energy(x,y,phi1,phi2):
    return ((x-y)**2)-math.cos(phi1-phi2)

factorized = False
  
twopi = 2*math.pi  

positions = [random.uniform(-2,2), random.uniform(-2,2)]
angles = [random.uniform(0,twopi),random.uniform(0,twopi)]

energies = []

N_steps = 10**7
space_step = 0.05
angle_step = twopi/50
beta = 1.0

distances = []
acceptance_index = 1

for index in range(N_steps):
    if index % 10000 == 0:
        print index
    if acceptance_index % 10000 == 0 and index != 0:
        print ("Positions: " + str(positions))
        print ("Angles: "+ str(angles))
        print ("Acceptanceratio :"+str(float(acceptance_index)/float(index)))
    r_move = random.choice([0,1])
    phi_move = random.choice([0,1])
    r_step = random.choice([-space_step,space_step])
    phi_step = random.choice([-angle_step,angle_step])
    delta_e_r = energy(positions[r_move]+r_step,positions[(r_move+1)%2],angles[phi_move],angles[(phi_move+1)%2])
    delta_e_phi = energy(positions[r_move],positions[(r_move+1)%2],angles[phi_move]+phi_step,angles[(phi_move+1)%2])
    delta_e_total = delta_e_r + delta_e_phi
    metrop = min(1,math.exp(-beta*delta_e_total))
    if factorized == True:
        metrop = min(1,math.exp(-beta*delta_e_r))*min(1,math.exp(-beta*delta_e_phi))
    if random.uniform(0.,1.) < metrop:
        acceptance_index += 1
        positions[r_move] += r_step
        angles[phi_move] = (angles[phi_move] + phi_step)%twopi
        
    energies.append(energy(positions[0],positions[1],angles[0],angles[1]))

print ("Mean energy: "+str(numpy.mean(energies)))
print ("Acceptanceratio :"+str(float(acceptance_index)/float(N_steps)))  


print("Duration: "+str(time.time()-time_start))
