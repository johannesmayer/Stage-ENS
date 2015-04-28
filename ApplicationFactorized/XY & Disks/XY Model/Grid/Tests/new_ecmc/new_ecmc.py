#!/usr/bin/python
##========+=========+=========+=========+=========+=========+=========+=
## PROGRAM : ecmc_XY_grid_spin.py
## PURPOSE : Event-chain simulation for XY on 2d grid
##           with periodic boundary conditions.
## VERSION : 05-MARCH-2015
## TYPE    : cython script
##========+=========+=========+=========+=========+=========+=========+
import cPickle, numpy, random, math
import os, sys 

def diff(x, y , L):
    return (x - y + L / 2.0) % L - L / 2.0

J = 1.0
beta = 1.2
L = 4
NIter = 20000
lth = 10.0 * math.pi
box = 2.0 * math.pi
Umax = 2.0 * J
C = []
for filename in os.listdir("./"):
    if filename.startswith("./ecmc_XY_grid_"+str(J)+"_"+str(L)+
                       "_"+str(beta)+"_"+str(lth)+".conf"):
        C = cPickle.load(open("./"+filename,'r'))

if len(C) == 0: C = [random.uniform(0.0, 2.0 * math.pi) for i in range(N ** 2)]
neighbours_all = [[(column + 1) % L + row * L, (column - 1) % L + row * L, 
                    column + ((row + 1) % L) * L, column + ((row - 1) % L) * L] 
                   for row in range(L) for column in range(L)]
print '\n',"starting"
for iter in range(NIter):
    if (iter + 1) % 10000==0: 
        print iter + 1, L, beta, lth
        cPickle.dump(C, open("./ecmc_XY_grid_"+str(J)+"_"+str(L)+"_"+
                             str(beta)+"_"+str(lth)+".conf" , "w" ))
    currentID = random.randint(0, L ** 2 - 1)
    l = lth
    while True:
        distanceToNextEvent = float("inf")
        moveSpin = C[currentID]
        neighbours = neighbours_all[currentID][:]
        while len(neighbours) > 0 : 
            k = neighbours.pop()
            fixSpin = C[k]
            diffA = diff(moveSpin, fixSpin, box)
            Estar = - math.log(random.uniform(0.0, 1.0)) / beta
            #this next two lines make the particle behave as if it was in the 
            #bottom of the valley and would get up with the help of Estar
            #because from now on one will always add J to Estar
            if diffA > 0: Estar += - J * math.cos(diffA)
            else: Estar += -J       
            #check how often it runs through the whole potential     
            distance_dummy = ((Estar + J) // Umax) * box
            Estar = (Estar + J) % Umax - J
            distance_dummy += - diffA + math.acos(- Estar / J)
            if distanceToNextEvent > distance_dummy: 
                distanceToNextEvent, nextID = distance_dummy, k
        if l < distanceToNextEvent:
            C[currentID] = (C[currentID] + l)%box
            chi = sum([math.cos(a - b) / L**2 for a in C for b in C])
            break
        else:
            C[currentID] = (C[currentID] + distanceToNextEvent)%box
            l -= distanceToNextEvent
            currentID = nextID
