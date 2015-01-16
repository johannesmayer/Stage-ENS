# -*- coding: utf-8 -*-

import math, random, numpy, time, sys

start_time = time.time()

def square_neighbors(L):
   N = L*L
   site_dic = {}
   x_y_dic = {}
   for j in range(N):
      row = j//L
      column = j-row*L
      site_dic[(row,column)] = j
      x_y_dic[j] = (row,column)
   nbr=[]
   for j in range(N):
      row,column = x_y_dic[j]
      right_nbr = site_dic[row,(column+1)%L]
      up_nbr = site_dic[(row+1)%L,column]
      left_nbr = site_dic[row,(column-1+L)%L]
      down_nbr = site_dic[(row-1+L)%L,column]
      nbr.append((right_nbr,up_nbr,left_nbr,down_nbr))
   nbr = tuple(nbr)
   return nbr,site_dic,x_y_dic


def energy(S,nbr):
    en = 0.0
    for index in range(len(S)):
        h = sum(S[nbr[index][j]] for j in range(4))
        en += -S[index]*h/2
    return en

def magnetisation(S):
    magn = numpy.mean(S)
    return magn   

def name_class(h,s):
    which_class = 0
    if s > 0:
       if h == 2:
           which_class = 1
       if h == 0:
           which_class = 2
       if h == -2:
           which_class = 3
       if h == -4:
           which_class = 4  
    else:
       which_class = name_class(h,-s) + 5
       
    return int(which_class)

def compute_classes(S,nbr):
    classes = [[] for k in range(10)]
    for j in range(len(S)):
        h = sum(S[nbr[j][k]][0] for k in range(4))
        which_class = name_class(h,S[j][0])
        classes[which_class].append(j)
        S[j][1] = which_class
    return classes        
 
def ffunction(number):
    return ((number + 5 ) % 10)
 
def towersample(tower):   
    eta = random.uniform(0.,max(tower))
    saturday_activity = 0
    for index in range(len(tower)):
        if eta < tower[index]:
            saturday_activity = index
            break
    return saturday_activity

def built_tower(probabilities):
    tow = []
    cumulative = 0.0
    for prob in probabilities:
        cumulative += prob
        tow.append(cumulative)     
    return tow

def built_probs(N,beta,is_fact):
    p = numpy.zeros(10)
    if is_fact == True:
        for k in range(10):
            if k < 5:
                p[k] =  (min(1.,math.exp(-2.*beta))**(4-k))
            else:
                p[k] = p[9-k] 
           
    if is_fact == False:                        
        for k in range(10):
            if k < 5:
                p[k] = (min(1,math.exp(-2*beta*(2-k))))
            else:
                p[k] = p[9-k]
    return p 

def f_function(class_number):
    value = (class_number+5)%10 
    return value  
 
def g_function(j,class_number):
    next_class = 0.0
    if j in range(0,5):
        next_class = class_number + 1
    if j in range(5,10):
        next_class = class_number -1
    return next_class
        
def magnetisation(S):
    spins = []
    for k in range(len(S)):
        spins.append(S[k][0])


    mag = numpy.mean(spins)
    return mag   
                 
def energy(S,nbr):
    ene = 0.0
    for index in range(len(S)):
        h = sum(S[nbr[index][j]][0] for j in range(4))
        ene += -h*S[index][0]/2
    return ene
############################################################################## 
""" 
use_factorized = sys.argv[1]

if use_factorized == "Factorized":
    use_factorized = True
if use_factorized == "Standard":
    use_factorized =False
""" 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
L = 6
N = L*L
#beta = sys.argv[2]



beta = 0.5
use_factorized = True

nbr, site_ic, x_y_dic = square_neighbors(L)
S = [[random.choice([-1,1]),0] for j in range(N)]

class_members = compute_classes(S,nbr)
probs = built_probs(N,beta,use_factorized)
current_probs = numpy.zeros(10)

curr_time = 0
flip_times = []

magnetisations = []
energies = []

time_max = 2**1





while curr_time < time_max:
    if curr_time // 10000 == 1:
        print("Time: "+str(curr_time)+"/"+str(time_max))
        print("Current Magnetisation: "+str(magnetisation(S)))
    #FIRST CALCULATE AT WHICH TIME TO FLIP THE FIRST SPIN
    for k in range(10):
        current_probs[k] = len(class_members[k])*probs[k] 
    reject = 1. - sum(current_probs)/float(N)
    if reject < 0.001:
        print("ATTENTION SMALL REJECT: "+str(reject))
    delta_t = 1
    if reject != 0:
        delta_t = 1 + int(math.log(random.uniform(0.,1.))/math.log(reject))
    
    curr_time = curr_time + delta_t
    flip_times.append(delta_t)
    
    mag = magnetisation(S)
    ene = energy(S,nbr)/float(N)
    
    len_mag = len(magnetisations)
        
    if curr_time <= time_max:
        magnetisations.extend([mag]*delta_t)
        energies.extend([ene]*delta_t)
    else:
        magnetisations.extend([mag]*(time_max-(curr_time-delta_t)))
        energies.extend([mag]*(time_max-(curr_time-delta_t))) 
    #TOWER SAMPLE WHICH CLASS SHOULD BE FLIPPED AND THEN TAKE A RANDOM SPIN OF THAT CLASS
    #REMOVE THAT SPIN FROM THAT CLASS AND SEND IT TO f(whichclass)
    which_class = towersample(built_tower(current_probs))
    flip_spin = random.choice(class_members[which_class])
    
    for neigh in nbr[flip_spin]:
        class_members[S[neigh][1]].remove(neigh)
        c_m = g_function(which_class,S[neigh][1])
        class_members[c_m].append(neigh)
        S[neigh][1] = c_m
    
    class_members[which_class].remove(flip_spin)
    class_members[f_function(which_class)].append(flip_spin)
    S[flip_spin][1] = f_function(which_class)
    S[flip_spin][0] = -S[flip_spin][0]
    
    
    
    
print("Average flipping time: "+str(numpy.mean(flip_times)))

print("Average magnetisation: "+str(numpy.mean(numpy.absolute(magnetisations))))
print("Average energy: "+str(numpy.mean(energies)))


print("Duration: "+str(time.time() - start_time))    
""" 
if use_factorized == True:
    numpy.save("DataAnalysis/SimulationData/fttc.fact.beta_"+str(beta)+".npy")
if use_factorized == False:
    numpy.save("DataAnalysis/SimulationData/fttc.stand.beta_"+str(beta)+".npy")
"""