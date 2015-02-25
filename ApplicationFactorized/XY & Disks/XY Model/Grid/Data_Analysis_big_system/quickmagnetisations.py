import numpy, sys, matplotlib.pylab as plt

def xy_magnetisation(spin_config):
    N = len(spin_config)
    if type(spin_config) != numpy.ndarray:
        spin_config = numpy.array(spin_config)
    mag = sum(numpy.exp(1j*spin_config))
    return mag/float(N)



if len(sys.argv) != 2:
    sys.exit('GIMME THE DATA')

data = numpy.load(sys.argv[1])


all_suscepts = []
N = len(data[0][0])

for config in data:
    all_suscepts.append(float(N) * abs( xy_magnetisation(config[0]) ) ** 2)


plt.plot(all_suscepts)
plt.show()