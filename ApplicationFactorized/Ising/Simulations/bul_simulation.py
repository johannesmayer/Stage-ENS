import math, random, numpy

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
    classes = numpy.zeros(10)
    for j in range(len(S)):
        h = sum(S[nbr[j][k]][0] for k in range(4))
        which_class = name_class(h,S[j][0])
        classes[which_class] += 1
        S[j][1] = which_class
    return classes        
 
    
L = 6
N = L*L

nbr, site_ic, x_y_dic = square_neighbors(L)
S = [[random.choice([-1,1]),0] for j in range(N)]

class_members = compute_classes(S,nbr)




