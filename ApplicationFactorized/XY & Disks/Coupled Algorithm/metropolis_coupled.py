import random, numpy, time, math, matplotlib.pyplot as plt

start_time = time.time()

def potential(config,moved,step):
    new_config = numpy.copy(config)
    new_config[moved] += step
    r = abs(new_config[0] - new_config[1])
    delta_phi = new_config[2] - new_config[3]
    pot = 0*r**2 - math.cos(delta_phi)    
    return pot
    
twopi = 2*math.pi
pi = math.pi


#positions = [random.uniform(-2,2) for k in range(2)]
#angles = [random.uniform(0.,twopi) for k in range(2)]


positions = [0.,0.]
angles = [0.,0.]


N_steps = 10**5
space_step = 0.1
angle_step = 0.1*math.pi
beta = 1.


distances = []
delta_phis = []
energies = []

testindex = 0

config = numpy.zeros(4)

poss_steps = [[space_step, -space_step], [angle_step, -angle_step]]


    
for index in xrange(N_steps):
    
    if index % 100000 == 0:
        print("PROGRESS: "+str(100*index/float(N_steps))+"%")

    move = random.randrange(4)
    step = random.choice(poss_steps[move//2])


    if random.uniform(0.,1.) < math.exp(-beta*(potential(config,move,step) - potential(config,move,0))):
        if move < 2 :
            config[move] += step
        else: config[move] = (config[move] + step) %twopi
        testindex += 1
    distances.append(config[0]-config[1])
    direct_dist = abs(config[2] - config[3])
    delta_phis.append(min(direct_dist, twopi-direct_dist))
    energies.append(potential(config,0,0))


#plt.plot(distances,"r-")
#plt.hist(angles,bins=100)
#plt.show()


print("Average distance: "+str(numpy.mean(distances))+"+-"+str(numpy.std(distances)/math.sqrt(len(distances))))
print("Average angle: "+str(numpy.mean(delta_phis))+"+-"+str(numpy.std(delta_phis)/math.sqrt(len(delta_phis))))
print("Average energy: "+str(numpy.mean(energies))+"+-"+str(numpy.std(energies)/math.sqrt(len(energies))))
print("Successrate: "+str(testindex/float(N_steps)))    


print("Duration: "+str(time.time()-start_time))