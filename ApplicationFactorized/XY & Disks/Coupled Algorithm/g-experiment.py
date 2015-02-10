import random, numpy, time, math, matplotlib.pyplot as plt

start_time = time.time()

def potential(phi1,phi2):

    delta_phi = phi1-phi2
    pot = -math.cos(delta_phi)
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


angles = [0.,0.]


N_steps = 10**7
angle_step = 0.05*math.pi
beta = 1.0

g = 0.3

lift = random.choice([0,1])
lift_g = [g, 1-g]

distances = []
delta_phis = []
energies = []

testindex = 0



for index in xrange(N_steps):
    
    if index % 100000 == 0:
        print("PROGRESS: "+str(100*index/float(N_steps))+"%")
        
    if random.uniform(0.,1.) < math.exp(-beta*(potential(angles[lift]+lift_g[0]*angle_step,angles[(lift+1)%2]+lift_g[1]*angle_step)-potential(angles[lift],angles[(lift+1)%2]))):
        angles[lift] = (angles[lift] + lift_g[0]*angle_step)%twopi
        angles[(lift+1)%2] = (angles[(lift+1)%2] + lift_g[1]*angle_step)%twopi
        testindex += 1

    else: lift = (lift+1)%2
    
    direct_dist = abs(angles[0] - angles[1])
    delta_phis.append(min(direct_dist, twopi-direct_dist)%pi)    
    energies.append(potential(angles[0],angles[1]))

#plt.plot(delta_phis,".")
"""
delta_phis = numpy.array(delta_phis)
index = delta_phis > 49.5*pi/float(50)
delta_phis[index] -= pi
"""

othername = numpy.arange(0,51)
lbin = othername*pi/float(50) - pi/float(100)
#print lbin
del_phi,b = numpy.histogram(delta_phis, bins=lbin, normed = True)

del_phi[0] *= 2

b = 0.5*(b[1:] + b[:-1])
print b

plt.grid()
#plt.plot(b,del_phi,".-")
#plt.plot(b,numpy.exp(numpy.cos(b))/3.97746)
plt.plot(b,del_phi - numpy.exp(numpy.cos(b))*del_phi[0]/numpy.exp(numpy.cos(0)))
plt.show()


print("Average angle: "+str(numpy.mean(delta_phis))+"+-"+str(numpy.std(delta_phis)/math.sqrt(len(delta_phis))))
print("Average energy: "+str(numpy.mean(energies))+"+-"+str(numpy.std(energies)/math.sqrt(len(energies))))
print("Successrate: "+str(testindex/float(N_steps)))    


print("Duration: "+str(time.time()-start_time))