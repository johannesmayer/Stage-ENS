#!/usr/bin/python

from random import uniform, randint, choice, seed
import pylab
import cPickle, numpy, math
from libc.math cimport acos, asin, sin, cos, sqrt, log
import os,sys 
cdef double pi = math.pi
#seed('test')

cdef double L = 4.2
cdef double sigma = 1 
cdef int N = 16
cdef int NIter = 10000
cdef double p = 0.9
cdef int indexPerp = 0
cdef int indexPar = 1

cdef int iter, k, currentID, nextID
cdef double movePx, movePy, movePa
cdef double fixPx, fixPy, fixPa
cdef double diffpara, diffperp, diffcollpar, diffcollperp

cdef double diff(double x, double y , double L):
    return (x - y + L/2.)%L - L/2.

if N>4 and int(sqrt(N))**2 ==N: C = [[i*L/sqrt(N)+(j%2)*0.5*sigma, j*L/sqrt(N)] for i in range(int(sqrt(N))) for j in range(int(sqrt(N)))]


for iter in range(NIter):
    if (iter+1)%10000==0:print iter+1,N,L
    if randint(0,1):indexPar, indexPerp = indexPerp, indexPar
    currentID = randint(0, N-1)
    l = log(uniform(0,1))/log(p) 
    while True: 
        distanceToNextEvent = float("inf")
        movePx, movePy = C[currentID]
        neighbours = range(currentID)+range(currentID+1,N)
        while len(neighbours)>0 :
            k = neighbours.pop()
            fixPx, fixPy = C[k]
            distance_dummy = float('inf')
            diffpara  =  diff(movePx, fixPx, L)
            diffperp  =  diff(movePy, fixPy, L)
            if indexPar : diffpara, diffperp = diffperp, diffpara
            if diffpara**2 + diffperp**2 <= sigma**2:
                if diffpara<0:
                    distanceToNextEvent, nextID = 0 , k
                    break                    
            if diffperp**2 >= sigma**2: continue
            Delta = sqrt(sigma**2 - diffperp**2)
            distance_dummy = (-diffpara-Delta)%L
            if distanceToNextEvent > distance_dummy:
                distanceToNextEvent, nextID = distance_dummy, k
                diffcollpar, diffcollperp = diffpara, diffperp
        u = min(l,distanceToNextEvent)
        l -= distanceToNextEvent
        C[currentID][indexPar] = (C[currentID][indexPar] +  u)%L
        if l <=0 : break 
        if uniform(0,1)<= min(1.,abs(diffcollperp/diffcollpara)):
            if diffperp>=0: currentID = nextID
            indexPar,indexPerp = indexPerp, indexPar
        else:currentID = nextID
cPickle.dump(C, open("data/ecmc_simple_"+str(L)+"_"+str(N)+"_"+str(p)+".conf" , "w" ))

