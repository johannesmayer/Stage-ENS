import numpy, random, time, math,matplotlib.pyplot as plt, sys

time_start = time.time()


beta = 1.0
position_step = 2.

all_collisions = []
some_positions = []

maximal_displacement = 100
n_times = 10**2

for index in range(n_times):
    
    initial_position = random.gauss(0,1/beta)
    velocity = random.choice([-1,1])    
    total_displacement = 0.0
    position = initial_position
    these_collisions = []
    these_collisions.append(initial_position)
    
    while total_displacement < maximal_displacement:
        
        upsilon = random.uniform(0.,1.)
        energy = -1/beta * math.log(upsilon)
        
        
        if position > 0 and velocity > 0:
            s = -abs(position) + math.sqrt(position**2 + 2*energy)
            if total_displacement + s > maximal_displacement:
                s = maximal_displacement - total_displacement
            position = position + s
            total_displacement += s
            
        if position < 0 and velocity > 0:
            s = abs(position) + math.sqrt(2*energy)
            if total_displacement + s > maximal_displacement:
                s = maximal_displacement - total_displacement
            position = position + s
            total_displacement += s
            
        if position > 0 and velocity < 0:
            s = abs(position) + math.sqrt(2*energy)
            if total_displacement + s > maximal_displacement:
                s = maximal_displacement - total_displacement
            position -= s
            total_displacement += s
            
        if position < 0 and velocity <0:
            s = -abs(position) + math.sqrt(position**2 + 2*energy)
            if total_displacement + s > maximal_displacement:
                s = maximal_displacement - total_displacement
            position -= s
            total_displacement += s
        
        velocity = -velocity
        these_collisions.append(position)
    """    
    my_index = 0
    while index < len(these_collisions)-1:
        pos = these_collisions[my_index]
        if numpy.sign(these_collisions[0]) != numpy.sign(these_collisions[1]):
            direction = numpy.sign(these_collisions[my_index+1] - these_collisions[my_index])
            if direction > 0:
                while pos + direction*position_step < these_collisions[my_index+1]:
                    some_positions.append(pos)
                    pos = pos + direction*position_step
                    
            if direction < 0:
                while pos + direction*position_step > tehse_collisions[my_index+1]:   
    #if the distance is positive then one has to move up if negative down!
    """
    
    all_collisions.extend(these_collisions)
        
    
    
plt.plot(all_collisions,'bo')
plt.show()



print("DURATION: "+str(time.time()- time_start))