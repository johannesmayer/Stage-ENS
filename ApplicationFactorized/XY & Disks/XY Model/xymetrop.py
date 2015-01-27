import random, numpy, time, math

def energy(phi1,phi2):
    ene = -1*math.cos(phi1 - phi2)
    return ene
############################################################################
starting_time = time.time()

spins = [random.uniform(0,2*math.pi),random.uniform(0,2*math.pi)]
spins = numpy.array(spins)

spin_difference = []
energies = []

N_steps = 10**7
spin_step = 2*math.pi/50
beta = 1.

twopi = 2*math.pi

acceptance_index = 0

for i_sweep in range(N_steps):
    #print spins/twopi
    move = random.choice([0,1])
    step = random.choice([-spin_step,spin_step])
    stay = spins[(move+1)%2]
    delta_E = energy((spins[move]+step),stay)-energy(spins[move],stay)
    if random.uniform(0.,1.) < min(1.,math.exp(-beta*delta_E)):
        acceptance_index += 1
        spins[move] = (spins[move]+step)%twopi
    spin_difference.append((spins[0]-spins[1]))
    energies.append(energy(spins[0],spins[1]))
    
####################################################################################    
    
print("Acceptance rate:"+str(acceptance_index/float(N_steps)))

print("Average Distance: "+str(numpy.mean(spin_difference)))
print("Average Energy: "+str(numpy.mean(energies)))

print("Duration: "+str(time.time()-starting_time))

