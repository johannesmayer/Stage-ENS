import numpy, math, random, time, matplotlib.pyplot as plt

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
    
def accept(p,beta,n1,n2):
    prob = min(1,(1-p)**(n1-n2)*math.exp(-2*beta*(n2-n1)))
    return prob

def fact_accept(p,beta,n1,n2):
    prob = ((min(1, math.exp(2*beta)*(1-p)))**n1)*((min(1, math.exp(-2*beta)/(1-p)))**n2)        
    return prob                    

def bunch(liste):
    old_list = liste[:]
    new_list = []
    while old_list != []:
        ele1 = old_list.pop()   
        ele2 = old_list.pop()
        new_list.append((ele1+ele2)/2)
    old_list = new_list[:]
    return old_list            

                  
       
L=6
N=L*L
beta=0.5
S=[random.choice([-1,1]) for k in range(N)]


acceptance_index = 0.0

factorized = True


N_iter = 2**16
N_bunches = 14
#p = 1-math.exp(-2*beta)
p = 0.6

energies = []
energy_errors = []

nbr,site_dic,x_y_dic=square_neighbors(L)
internal_energy = energy(S,nbr)

for i_sweep in range(N_iter):
    if i_sweep % 1000 == 0:
        print("Progress: "+str(i_sweep)+"/"+str(N_iter))
    y=random.randint(0,N-1)
    pocket = [y]
    cluster = [y]
    outer_edge = []
    N_cluster = 1
    while pocket != []:
        k = random.choice(pocket)
        for l in nbr[k]:
            if S[l] == S[k]:
                if random.uniform(0.,1.) < p:
                    if l not in cluster:
                        pocket.append(l)
                        cluster.append(l)
                        N_cluster += 1
                elif l not in outer_edge:
                    outer_edge.append(l)
            elif l not in outer_edge:
                outer_edge.append(l)
        pocket.remove(k)
        for spin in cluster:
            if spin in outer_edge:
                outer_edge.remove(spin) 
    n_one= 0.0
    n_two= 0.0
    #recall that n_1+n_2 != len(outer_edge) because of outer edge spins with multiple neighbors
    for l in outer_edge:
        for k in nbr[l]:
            if k in cluster:
                if S[l]==S[k]:
                    n_two += 1
                else:
                    n_one += 1 
    #here the acceptance probability is introduced
    #print(fact_accept(p,beta,n_one,n_two))
    upsilon = 0.0
    if factorized == True:
        upsilon = fact_accept(p,beta,n_one,n_two)
    else:
        upsilon = accept(p,beta,n_one,n_two)
        
    if random.uniform(0.,1.) < upsilon:
        acceptance_index += 1
        for k in cluster:
            S[k] = -S[k]
        internal_energy = internal_energy + 2*n_two - 2*n_one
    #energies.append(energy(S,nbr))
    energies.append(internal_energy/N)

for index in range(N_bunches):
    energies = bunch(energies)
    energy_errors.append(numpy.std(energies)/math.sqrt(len(energies)))


print("Mean energy per particle: "+str(numpy.mean(energies))) 
print("Cluster flip Acceptance:"+str(acceptance_index/N_iter))   
    
print("Duration: "+str(time.time()-start_time))  


####### PLOTTING SECTION #############



##### PLOT TO SEE THE BUNCHING ALGORITHMS RESULTS #########

bunch_list = numpy.arange(1,N_bunches+1)
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.plot(bunch_list,energy_errors,'go')
if factorized == True:
    ax1.set_title("Error of factorized Cluster at p="+str(p)+" and N="+str(N_iter)) 
if factorized == False:
    ax1.set_title("Error of Cluster at p="+str(p)+" and N="+str(N_iter)) 
ax1.set_xlabel("# applications of Bunching algorithm")
ax1.set_ylabel("Statistical Error of mean energy")
fig1.show()



