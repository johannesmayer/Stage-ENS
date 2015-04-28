import numpy, random, math, time, sys, os

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
    
def magnetisation(S):
    magn = numpy.mean(S)
    return magn
    

if len(sys.argv) != 3:
    sys.exit("############# WRONG INPUT ############## GIVE ME THE INPUT <Standard/Factorized> _ <beta>")



factorized = sys.argv[1]

if factorized == "Standard":
    factorized = False
if factorized == "Factorized":
    factorized = True
                              
N_iter = 2**3


L = 6
N = L*L

beta = float(sys.argv[2])


outdir = 'data'
if not os.path.isdir(outdir):
    os.makedirs(outdir)
ID = 'ising'+factorized+'_%f_%i_'%(beta,L)
filename = outdir + '/' + ID + '.npy'


#beta = math.log(1+math.sqrt(2))/2
#beta = 0.1

nbr, site_dic, x_y_dic = square_neighbors(L)
S=[random.choice([-1,1]) for k in range(N)]


accept_index = 0.0

internal_energy = energy(S,nbr)

energies = []
magnetisations = []


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
    magnetisations.append(numpy.absolute(magnetisation([S])))
    
print("Internal Energy pp: " + str(numpy.mean(energies)))
print("Magnetisation pp: " + str(numpy.mean(magnetisations)))
print("acceptance ratio: " + str(accept_index/N_iter))       
            
    
print("Duration: "+str(time.time() - start_time))    

local = [energies, magnetisations]

if factorized == True:
    numpy.save("DataAnalysis/SimulationData/local_fact_beta_"+str(beta)[:6]+".npy",local)
    
    
if factorized == False:
    numpy.save("DataAnalysis/SimulationData/local_stand_beta_"+str(beta)[:6]+".npy",local)
   

    
