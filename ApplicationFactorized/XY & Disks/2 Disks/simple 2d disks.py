import random, numpy, time, math

start_time = time.time()

def potential(x1,x2):
    r = abs(x1-x2)
    return 1/r + r**2
    

positions = [random.uniform(-2,2), random.uniform(-2,2)]

N_steps = 10**5
space_step = 0.1
beta = 1.0

distances = []

for index in range(N_steps):
    move = random.choice([0,1])
    step = random.choice([-space_step,space_step])
    metrop = min(1,math.exp(-beta*(potential(positions[move]+step,positions[(move+1)%2])-potential(positions[move],positions[(move+1)%2]))))
    if random.uniform(0.,1.) < metrop:
        positions[move] += step 
    distances.append(abs(positions[0]-positions[1]))

print("Average distance: "+str( numpy.mean(distances)))
    


print("Duration: "+str(time.time()-start_time))