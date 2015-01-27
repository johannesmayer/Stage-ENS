import numpy, random, time, math,matplotlib.pyplot as plt, sys

time_start = time.time()


twopi = 2*math.pi


all_collisions =[[],[]]
initial_angles = [random.uniform(0,twopi),random.uniform(0,twopi)]

first_lift = random.choice([0,1])

angles = initial_angles

delta_phi = angles[0] - angles[1]

######################################################################################
"""
If delta_phi smaller zero and phi1 has the lift move left in the valley
and if phi2 has the lift move right in the valley.
If delta_phi is bigger than zero and phi1 has the lift move right in the valley
If delta_phi is bigger tahn zero and phi2 has the lift move left in the valley!
"""
######################################################################################













print("DURATION: "+str(time.time()- time_start))