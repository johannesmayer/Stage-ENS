import random, numpy, time, math

start_time = time.time()

def potential(x1,x2):
    pot = -math.cos(x1-x2)
    return pot
    
twopi = 2*math.pi
################################################################################
spins = [random.uniform(0,twopi), random.uniform(0,twopi)]

N_steps = 10**6
step = twopi/10
beta = 1.0

distances = []
energies = []
lift = random.choice([0,1])

accept = 0

for index in range(N_steps):
  
    metrop = min(1,math.exp(-beta*(potential(spins[lift]+step,spins[(lift+1)%2])-potential(spins[lift],spins[(lift+1)%2]))))
    if random.uniform(0.,1.) < metrop:
        accept += 1
        spins[lift] = (spins[lift] + step)%twopi
    else: lift = (lift+1)%2
    distances.append(spins[0]-spins[1])
    energies.append(potential(spins[0],spins[1]))

################################################################################

print("Acception ratio: "+str(accept / float(N_steps)))

print("Average distance: "+str( numpy.mean(distances)))
print("Average energy: "+str(numpy.mean(energies)))


print("Duration: "+str(time.time()-start_time))