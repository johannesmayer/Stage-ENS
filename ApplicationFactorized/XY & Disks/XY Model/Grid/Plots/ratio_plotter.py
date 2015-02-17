import matplotlib.pylab as plt
import numpy


ratios = numpy.array([32.9, 42.8, 59.9])
Ns = numpy.array([20.0**2,30.0**2,40.0**2])

plt.plot(Ns, ratios)
plt.show()