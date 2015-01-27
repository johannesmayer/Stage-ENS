import numpy, random, math
from scipy.integrate import quad
from scipy.optimize import fsolve
from scipy.misc import derivative


def potential(x):
    return 0.5*x**(2)

def deriv_pot(x):
    return derivative(potential,x)
"""    
def integrand(t,position,velocity):
    return max(0,deriv_pot(position+velocity*t))
"""
def integrand(t,position,velocity):
    return max(0,velocity*(position+velocity*t))
    
def func(s,s_0,velocity,randomlog):
    integral, err = quad(integrand,s_0,s,args = (s_0,velocity))
    return integral - randomlog

position = 0
velocity = +1

beta = 0.5
positions = []
n_turns = 10**5

for index in range(n_turns):
    if index % 100 == 0:
        print("Progress: "+str(index)+"/"+str(n_turns))
    upsilon = random.uniform(0,1)
    randomlog = -1/beta * math.log(upsilon)

    sol = fsolve(func,1.,args = (0,velocity,randomlog))
    if sol[0] == 1:
        print ("NIX WARS")
    #print("Step: "+str(sol[0]*velocity))
    position = position + velocity*sol[0]
    #print("Position: "+str(position))
    velocity = -velocity


    positions.append(position)

print numpy.mean(positions)


