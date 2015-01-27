import random, numpy, time, math

start_time = time.time()

def potential(x1,x2):
    r = abs(x1-x2)
    return 1/r + r**2
    

positions = [random.uniform(-2,2), random.uniform(-2,2)]

N_steps = 10**5
step = 0.1
beta = 0.5
lift = []
distances = []
lift = random.choice([0,1])

for index in range(N_steps):
    metrop = min(1,math.exp(-beta*(potential(positions[lift]+step,positions[(lift+1)%2])-potential(positions[lift],positions[(lift+1)%2]))))
    if random.uniform(0.,1.) < metrop:
        positions[lift] += step 
    else: lift = (lift+1)%2
    distances.append(abs(positions[0]-positions[1]))

print("Average distance: "+str( numpy.mean(distances)))
    


print("Duration: "+str(time.time()-start_time))