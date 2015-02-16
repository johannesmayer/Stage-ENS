import numpy, math, random, matplotlib.pylab as plt

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
 
   
def partners_at_distance(site, distance, L, site_dic, x_y_dic, directions):
    # this function gives for a given site all partners at the given (integer) distance
    # in all given directions one wants to look at
    if distance == 0:
        return [site]
    else:
        coord = numpy.array(x_y_dic[site])
        partners = []
        for direct in directions:
            partners.append(site_dic[tuple((coord + distance*direct)%L)])
        return partners
      
        
          
              
L = 55
N = L**2

nbr, site_dic, x_y_dic = square_neighbors(L)
directions = [numpy.array((1,0)),numpy.array((0,1)),numpy.array((-1,0)),numpy.array((0,-1))]

spins = numpy.zeros(N)
for position in xrange(N):
    if position % 2 == 0:
        spins[position] = random.uniform(0.,1.)
for position in xrange(N):
    if position % 2 == 1:
        spins[position] = sum(spins[neigh] for neigh in nbr[position])/float(4)
print spins           
            

spin_mean = numpy.mean(spins)


maximal_distance = int(float(L)/2)   

all_distances = numpy.arange(maximal_distance)

correlator = []

for distance in all_distances:
    one_dist_list = []
    for site in xrange(N):
        for partner in partners_at_distance(site, distance,L, site_dic, x_y_dic, directions):
            one_dist_list.append(spins[site]*spins[partner])
    correlator.append(numpy.mean(one_dist_list))
correlator = numpy.array(correlator)

plt.plot((correlator - spin_mean**2 )/(numpy.var(spins)))
plt.yscale('log')
plt.show()
    
    