# -*- coding: utf-8 -*-

import math, random, numpy, time, sys, matplotlib.pyplot as plt

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

def built_probs(N,beta,use_fact):
    p = numpy.zeros(10)
    if use_fact == True:
        for k in range(10):
            if k < 5:
                p[k] =  (min(1.,math.exp(-2.*beta))**(4-k))
            else:
                p[k] = p[9-k] 
           
    if use_fact == False:                        
        for k in range(10):
            if k < 5:
                p[k] = (min(1,math.exp(-2*beta*(4-2*k))))
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
    
def energy_change(S):
    h_class = 0.
    bkl_class = S[1] % 5
    if bkl_class == 0:
        h_class = 4
    if bkl_class == 1:
        h_class = 2
    if bkl_class == 3:
        h_class = -2
    if bkl_class == 4:
        h_class = -4
    return 2*h_class*S[0]
    
    
############################################################################## 

if len(sys.argv) != 4:
    sys.exit("WRONG INPUT! ############ GIVE ME THE INPUT IN THE ORDER: <Factorized/Standard> _ <BETA> _ <EXPONENT OF 2**x FOR T_MAX>")

use_factorized = sys.argv[1]

is_fact = "fact"
if use_factorized == "Factorized":
    use_factorized = True
if use_factorized == "Standard":
    use_factorized =False
    is_fact = "stand"

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
L = 6
N = L*L
beta = float(sys.argv[2])



#beta = 4.
#use_factorized = False

nbr, site_ic, x_y_dic = square_neighbors(L)
S = [[random.choice([-1,1]),0] for j in range(N)]

class_members = compute_classes(S,nbr)
probs = built_probs(N,beta,use_factorized)
current_probs = numpy.zeros(10)

curr_time = 0

flip_times = []
magnetisations = []
energies = []

curr_energy = energy(S,nbr)/float(N)
curr_magnet = magnetisation(S)

#time_max = 2**34
time_max = 2**int(sys.argv[3])

while curr_time < time_max:
    if curr_time % 10000 == 1:
        print("Time: "+str(curr_time)+"/"+str(time_max))
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

            
    if curr_time <= time_max:
        flip_times.append(delta_t)
        magnetisations.append(curr_magnet)
        energies.append(curr_energy)
    else:
        flip_times.append(time_max-(curr_time-delta_t))
        magnetisations.append(curr_magnet)
        energies.append(curr_energy)
        
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
    
    curr_magnet = curr_magnet - 2*S[flip_spin][0]/float(N)
    curr_energy = curr_energy + energy_change(S[flip_spin])/float(N)
    
    
    S[flip_spin][1] = f_function(which_class)
    S[flip_spin][0] = -S[flip_spin][0]
    
energies = numpy.array(energies)
magnetisations = numpy.array(magnetisations)
flip_times = numpy.array(flip_times)

avg_mag = (1/float(time_max))*numpy.sum(magnetisations*flip_times)
avg_ene = (1/float(time_max))*numpy.sum(energies*flip_times)
 
       
print("Average flipping time: "+str(numpy.mean(flip_times)))

print("Average magnetisation: "+str(avg_mag))
print("Average energy: "+str(avg_ene))

#plt.plot(energies,'b-')
#plt.show()

result = numpy.array([flip_times,energies,numpy.absolute(magnetisations)])

print("Duration: "+str(time.time() - start_time))    


path = "DataAnalysis/SimulationData/fttc."+is_fact+".beta_"+str(beta)[:5]+"tmax_"+str(time_max)+".npy"


numpy.save(path,result)

print("DATA SAVED IN "+path)