import numpy, random, math, time, sys

start_time = time.time()

def spinglass_square_neighbors(L):
    N = L*L
    site_dic = {}
    x_y_dic = {}
    coupling_dic = {}
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
    for j in range(N):
        for k in range(4):
            if tuple(sorted((j,nbr[j][k]))) not in coupling_dic.keys():
                coupling_dic[tuple(sorted((j,nbr[j][k])))] = random.choice([-1,1])
            
    return nbr,site_dic,x_y_dic, coupling_dic
    
def energy(S,nbr,coupling_dic):
    ene = 0.0
    for index in range(len(S)):
        h = sum(S[nbr[index][j]]*coupling_dic[tuple(sorted((index,nbr[index][j])))] for j in range(4))
        ene += -h*S[index]/2
    return ene
    
def magnetisation(S):
    magn = numpy.mean(S)
    return magn

    
use_factorized = [True,False]

N_iter = 2**20

L = 6
N = L*L
beta = float(sys.argv[1])
#beta = math.log(1+math.sqrt(2))/2
#beta = 0.5

nbr, site_dic, x_y_dic, coupling_dic = spinglass_square_neighbors(L)

initial_S=[random.choice([-1,1]) for k in range(N)]

for factorized_algo in use_factorized:
    if factorized_algo == True:
        algotype = "Factorized "
    if factorized_algo == False:
        algotype = "Standard "
    S = initial_S[:]
    internal_energy = energy(S,nbr, coupling_dic)
    
    energies = []
    magnetisations = []
    
    accept_index = 0.0
    
    for i_sweep in range(N_iter):
        if i_sweep % 1000 == 0:
            print("Progress: "+str(i_sweep)+"/"+str(N_iter))
        #here pick a random spin and look at the surroundings
        k=random.randint(0,N-1)
        h = sum(S[nbr[k][j]]*coupling_dic[tuple(sorted((k,nbr[k][j])))] for j in range(4))
        upsilon = 0.0
        if factorized_algo == True:
            del_ener = []
        #look what energy difference a flip of the chosen spin would make with each 
        #of its neighbours
            for j in range(4):
                del_ener.append(2*S[nbr[k][j]]*S[k]*coupling_dic[tuple(sorted((k,nbr[k][j])))])
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
        magnetisations.append(magnetisation([S]))
        
    print(algotype+"Internal Energy pp: " + str(numpy.mean(energies)))
    print(algotype+"Magnetisation pp: " + str(numpy.mean(magnetisations)))
    print(algotype+"acceptance ratio: " + str(accept_index/N_iter))       
                
        
    print("Duration: "+str(time.time() - start_time))    
    
    local = [energies, magnetisations]
    
    if factorized_algo == True:
        numpy.save("DataAnalysis/SimulationData/spinglass_local_fact_beta_"+str(beta)+".npy",local)
        
    if factorized_algo == False:
        numpy.save("DataAnalysis/SimulationData/spinglass_local_stand_beta_"+str(beta)+".npy",local)
    
    
        
