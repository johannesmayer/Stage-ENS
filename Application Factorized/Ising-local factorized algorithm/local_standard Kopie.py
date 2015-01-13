import math, numpy, random, matplotlib.pylab as plt, time

starting_point = time.time()

def square_neighbors(L):
    N = L*L
    site_dic = {}
    x_y_dic = {}
    for j in range(N):
        row = j // L 
        column = j - row * L 
        site_dic[(row,column)] = j
        x_y_dic[j] = (row, column)
    nbr = []
    for j in range(N):
        row, column = x_y_dic[j]
        #das sind jetzt die pbc
        right_nbr = site_dic[row,(column+1)%L]
        left_nbr = site_dic[row,(column-1+L)%L]
        up_nbr = site_dic[(row+1)%L,column]
        down_nbr = site_dic[(row-1+L)%L,column]
        nbr.append((right_nbr,up_nbr,left_nbr,down_nbr))
    nbr = tuple(nbr)
    #rueckgabe sind ein tupel mit nachbarn und zwei dictionaries
    return nbr, site_dic, x_y_dic

def energy(S,nbr):
    ene = 0.0
    for index in range(len(S)):
        h = sum(S[nbr[index][j]] for j in range(4))
        ene += -h*S[index]
    return ene

def bunch(liste,times):
    old_list = liste[:]
    new_list = []
    for index in range(times):
        while old_list != []:
            ele1 = old_list.pop()   
            ele2 = old_list.pop()
            new_list.append((ele1+ele2)/2)
        old_list = new_list[:]
        new_list = []
    return old_list
            
                
def uncert(liste):
    first = numpy.asarray(liste)
    second = first*first
    uncert = numpy.mean(second) - numpy.mean(first)*numpy.mean(first)
    return uncert
    
def heat_cap(N_part,beta,liste):
    return uncert(liste)*(beta**2)/N_part                            

def heat_cap_err(N_part,beta,liste):
    en = numpy.asarray(liste) 
    ensq = en**2
    en_err = numpy.std(en)/math.sqrt(len(en))
    ensq_err = numpy.std(ensq)/math.sqrt(len(ensq))
    return (beta**2)*math.sqrt(ensq_err**2 + (2*numpy.mean(en)*en_err)**2)/N_part
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
L = 6
N= L*L
N_iterations = 2**20
N_bunches = 1
S_init = [random.choice([-1,1]) for k in range(N)]

temperatures = numpy.array([0.5,1.,1.5,2.,2.5,3.,3.5,4.])
betas = 1./temperatures
#betas = numpy.array([10.])

exact_energies = numpy.array( [-1.999,-1.997,-1.951,-1.747,-1.280,-0.887,-0.683,-0.566])
exact_capacities = numpy.array([0.00003,0.02338,0.19758,0.68592,1.00623,0.55665,0.29617,0.18704])



energy_variances = []
bunch_indices = []

en_per_part = []

energies = []
en_errors = []

capacities = []
cap_errors = []



nbr, site_dic, x_y_dic = square_neighbors(L)

for beta in betas:
    S = S_init[:]
    initial_energy = energy(S,nbr)
    energies.append(initial_energy)
    for iter in range(N_iterations):
        k=random.randint(0,N-1)
        h=sum(S[nbr[k][j]] for j in range(4))
        Delta_E = 2*h*S[k]
        Upsilon = math.exp(-beta*Delta_E)
        if random.uniform(0.,1.)<Upsilon: 
            S[k] = -S[k]
            initial_energy = initial_energy + Delta_E
            energies.append(initial_energy)
        else:
            energies.append(initial_energy)
    en_per_part.append(numpy.mean(energies)/float(N))
    capacities.append(heat_cap(N,beta,energies))  
    energies = []            
en_diff = abs(numpy.asarray(en_per_part)- exact_energies)
cv_diff = abs(numpy.asarray(capacities)- exact_capacities)
                                                                
for index in range(N_bunches+1):
    bunch_indices.append(index)
    temp_list = bunch(energies,index)
    cap_errors.append(heat_cap_err(N,beta,temp_list))
    en_errors.append(numpy.std(temp_list)/math.sqrt(len(temp_list)))



fig0 = plt.figure()
ax0 = fig0.add_subplot(111)
ax0.plot(temperatures,en_per_part,'go',label='energy pp')
ax0.plot(temperatures,exact_energies,'bo',label='exact energies')
ax0.plot(temperatures,en_diff,'ro',label='difference')
ax0.set_xlabel("Temperature")
ax0.set_ylabel("internal energy pp")
ax0.set_title("Comparison with exact results: internal energy")
ax0.legend()
fig0.show()

fig01 = plt.figure()
ax01 = fig01.add_subplot(111)
ax01.plot(temperatures,capacities,'go',label='heat capacity')
ax01.plot(temperatures,exact_capacities,'bo',label='exact capacities')
ax01.plot(temperatures,cv_diff,'ro',label='difference')
ax01.set_xlabel("Temperature")
ax01.set_ylabel("heat capacity c_V pp")
ax01.set_title("Comparison with exact results: heat capacity")
ax01.legend()
fig01.show()

"""
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.plot(bunch_indices,en_errors,'ro')
ax1.set_title("Statistical error of the internal energy")
ax1.set_xlabel("Applications of the bunching algorithm")
ax1.set_ylabel("Statistical Error")
fig1.show()

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.plot(bunch_indices,cap_errors,'bo')
ax2.set_title("Statistical error of the heat capacity")
ax2.set_xlabel("Applications of the bunching algorithm")
ax2.set_ylabel("Statistical Error")
fig2.show()
"""

print("Laufzeit: " + str(time.time()-starting_point))

































