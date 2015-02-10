import random, numpy, time, math, matplotlib.pyplot as plt

start_time = time.time()

def potential(x1,x2,phi1,phi2):
    r = abs(x1-x2)
    delta_phi = phi1-phi2
    pot = r**2 - r*math.cos(delta_phi)
    return pot
  
def step_choice(space_step, angle_step, steps):
    steps[0] = random.choice([0,space_step])
    steps[1] = random.choice([0,angle_step])
    if steps[0] == 0 and steps[1] == 0:
        step_choice(space_step, angle_step, steps)
    return steps    
 
twopi = 2*math.pi
pi = math.pi


#positions = [random.uniform(-2,2) for k in range(2)]
#angles = [random.uniform(0.,twopi) for k in range(2)]


positions = [0.,0.]
angles = [0.,0.]


N_steps = 10**6
space_grid = 0.1
angle_grid = 0.1*math.pi
beta = 1.0

lift = random.choice([0,1])

distances = []
delta_phis = []
energies = []

testindex = 0


steps = [space_grid,angle_grid]

for index in xrange(N_steps):
    
    if index % 100000 == 0:
        print("PROGRESS: "+str(100*index/float(N_steps))+"%")
    
    if index % 100 == 0:
        steps = step_choice(space_grid, angle_grid, steps)
    space_step = steps[0]
    angle_step = steps[1]    
            
    
    if random.uniform(0.,1.) < math.exp(-beta*(potential(positions[lift]+space_step,positions[(lift+1)%2],angles[lift]+angle_step,angles[(lift+1)%2])-potential(positions[lift],positions[(lift+1)%2],angles[lift],angles[(lift+1)%2]))):
        positions[lift] += space_step
        angles[lift] = (angles[lift] + angle_step)%twopi
        testindex += 1
        
    else: lift = (lift+1)%2
    
    distances.append(positions[0]-positions[1])
    direct_dist = abs(angles[0] - angles[1])
    delta_phis.append(min(direct_dist, twopi-direct_dist))    
    energies.append(potential(positions[0],positions[1],angles[0],angles[1]))

#plt.plot(delta_phis,"r.")
#plt.hist(angles,bins=100)
#plt.show()


print("Average distance: "+str(numpy.mean(distances))+"+-"+str(numpy.std(distances)/math.sqrt(len(distances))))
print("Average angle: "+str(numpy.mean(delta_phis))+"+-"+str(numpy.std(delta_phis)/math.sqrt(len(delta_phis))))
print("Average energy: "+str(numpy.mean(energies))+"+-"+str(numpy.std(energies)/math.sqrt(len(energies))))
print("Successrate: "+str(testindex/float(N_steps)))    


print("Duration: "+str(time.time()-start_time))