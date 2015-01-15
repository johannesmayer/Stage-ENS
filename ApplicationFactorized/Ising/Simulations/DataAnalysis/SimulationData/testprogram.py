import numpy, matplotlib.pyplot as plt, sys

en, mag = numpy.load(sys.argv[1]) 

plt.plot(mag[:100000])
plt.show()