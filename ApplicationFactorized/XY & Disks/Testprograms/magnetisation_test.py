import cmath, numpy, random


def xy_magnetisation(spin_config):
    N = len(spin_config)
    if type(spin_config) != numpy.ndarray:
        spin_config = numpy.array(spin_config)
    mag = sum(numpy.exp(1j*spin_config))
    return mag/float(N)
    
def vect_mag_direction(magnetis):
    r = abs(magnetis)
    phi = cmath.phase(magnetis)
    mag = r*numpy.array([numpy.cos(phi),numpy.sin(phi)])
    print mag
    return mag
    
N = 3
config = [random.uniform(0.,2*cmath.pi) for k in xrange(N)]

print 
