import random, numpy, time, math

def energy(phi1,phi2):
    ene = -1*math.cos(phi1 - phi2)
    return ene



spins = [random.uniform(0,2*math.pi),random.uniform(0,2*math.pi)]
spins = numpy.array(spins)
spin_difference = []

N_steps = 10**6
spin_step = 2*math.pi/5
beta = 1.

twopi = 2*math.pi

acceptance_index = 0

lift = random.choice([0,1])

for i_sweep in range(N_steps):
    move = spins[lift]  
    stay = spins[(move+1)%2]
    delta_E = energy(move+spin_step,stay)-energy(move,stay)
    if random.uniform(0.,1.) < min(1.,math.exp(-beta*delta_E)):
        acceptance_index += 1
        spins[lift] = (spins[lift]+spin_step)%twopi
    else:
        lift = (lift+1)%2
    spin_difference.append((spins[0]-spins[1]))
    
print("Acceptance rate:"+str(acceptance_index/float(N_steps)))

print("Average Distance: "+str(numpy.mean(spin_difference)))
print("Error Estimate: "+str((1/math.sqrt(float(N_steps)))*numpy.var(spin_difference)))