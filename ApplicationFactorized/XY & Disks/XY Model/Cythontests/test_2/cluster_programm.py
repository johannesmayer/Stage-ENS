import time, math, random, numpy
from cluster_functions import random_uniform_on_sphere

def rizze(dim):
    sigma = 1/math.sqrt(dim)
    unit_vec = numpy.array([random.gauss(0,sigma) for index in xrange(dim)])
    unit_vec /= math.sqrt(sum(unit_vec**2))
    return unit_vec

print 'a'

N = 25000
test_start_1 = time.time()

for index in range(N):
    a = random_uniform_on_sphere(2)

print 'cythontime: '+str(time.time()- test_start_1)

st = time.time()
for index in range(N):
    a = rizze(2)
print'ssss', time.time()-st
