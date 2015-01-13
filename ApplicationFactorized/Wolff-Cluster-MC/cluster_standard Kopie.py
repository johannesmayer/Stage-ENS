import numpy, math, random, time

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
    
L=6
N=L*L
S=[random.choice([-1,1]) for k in range(N)]
beta=0.5
nbr,site_dic,x_y_dic=square_neighbors(L)
energies = []

acceptance_index = 0.0

#p = 1-math.exp(-2*beta)
p = 0.6
N_iter = 10**4

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
    if random.uniform(0.,1.) < accept(p,beta,n_one,n_two):
    #if random.uniform(0.,1.) < fact_accept(p,beta,n_one,n_two):
        acceptance_index += 1
        for k in cluster:
            S[k] = -S[k]
        internal_energy = internal_energy + 2*n_two - 2*n_one
    #energies.append(energy(S,nbr))
    energies.append(internal_energy)
print("Mean energy per particle: "+str(numpy.mean(energies)/N)) 
print("Cluster flips :"+str(acceptance_index/N_iter))   
    
print("Duration: "+str(time.time()-start_time))  