import numpy, random, math, time, matplotlib.pyplot as plt

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
    nbr = []
    for j in range(N):
        row,column = x_y_dic[j]
        right_nbr = site_dic[(row,(column+1)%L)]
        left_nbr = site_dic[(row,(column-1+L)%L)]
        up_nbr = site_dic[((row-1+L)%L,column)]
        down_nbr = site_dic[((row+1)%L,column)]
        nbr.append((right_nbr,left_nbr,up_nbr,down_nbr))
    nbr = tuple(nbr)
    return nbr,site_dic,x_y_dic
    
def energy(S,nbr):
    ene = 0.0
    for index in range(len(S)):
        h = sum(S[nbr[index][j]] for j in range(4))
        ene += -h*S[index]/2
    return ene
    
    

def bunch(liste):
    old_list = liste[:]
    new_list = []
    while old_list != []:
        ele1 = old_list.pop()   
        ele2 = old_list.pop()
        new_list.append((ele1+ele2)/2)
    old_list = new_list[:]
    return old_list            
              
        
factorized = False
        
N_iter = 2**20  
N_bunches = 19

L = 6
N = L*L
beta = 0.5


nbr, site_dic, x_y_dic = square_neighbors(L)
S=[random.choice([-1,1]) for k in range(N)]


accept_index = 0.0

internal_energy = energy(S,nbr)

energies = []
energy_errors = []

for i_sweep in range(N_iter):
    if i_sweep % 1000 == 0:
        print("Progress: "+str(i_sweep)+"/"+str(N_iter))
    #here pick a random spin and look at the surroundings
    k=random.randint(0,N-1)
    h = sum(S[nbr[k][j]] for j in range(4))
    upsilon = 0.0
    if factorized == True:
        del_ener = []
    #look what energy difference a flip of the chosen spin would make with each 
    #of its neighbours
        for j in range(4):
            del_ener.append(2*S[nbr[k][j]]*S[k])
    #apply the factorized metropolis p_acc(a->b) = prod(min(1,exp(-beta*delta(E_ij)))
        bracket_sum = 0.0
        for iter in range(4):
            bracket_sum += max(0,del_ener[iter])        
        upsilon = math.exp(-beta*bracket_sum)
    else:
        upsilon = min(1,math.exp(-beta*2*S[k]*h))
    if random.uniform(0.,1.) < upsilon:
        S[k] = -S[k]
        # delta E = 2 * oldspin * h so since we flipped we have to subtract 2hS[k]
        internal_energy = internal_energy - 2*h*S[k]
        accept_index += 1
    energies.append(internal_energy/N)

print("Internal Energy pp: " + str(numpy.mean(energies)))
print("acceptance ratio: " + str(accept_index/N_iter))
        
            
    
print("Duration: "+str(time.time() - start_time))    
    
    
for index in range(N_bunches):
    energies = bunch(energies)
    energy_errors.append(numpy.std(energies)/math.sqrt(len(energies)))
    
    
    



####### PLOTTING SECTION #############



##### PLOT TO SEE THE BUNCHING ALGORITHMS RESULTS #########

bunch_list = numpy.arange(1,N_bunches+1)
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.plot(bunch_list,energy_errors,'go')

if factorized == True:
    ax1.set_title("Error of factorized local at N="+str(N_iter)) 
if factorized == False:
    ax1.set_title("Error of standard local at N="+str(N_iter)) 
ax1.set_xlabel("# applications of Bunching algorithm")
ax1.set_ylabel("Statistical Error of mean energy")

fig1.show()

    
    
    
    
    
