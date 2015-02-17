import matplotlib.pyplot as plt
import numpy

event_mag = numpy.array([0.579,0.493,0.448,0.420,0.0])
markov_mag = numpy.array([0.580,0.485,0.458, 0.416,0.0])

difference = markov_mag - event_mag

ratio = []

markov_errors =numpy.array([0.0057,0.0059,0.0092,0.005,0.0])
event_errors = numpy.array([0.0008,0.00118,0.0012,0.001,0.0])

difference_error = numpy.sqrt(markov_errors**2 + event_errors**2)

L = [10, 20 ,30,40,50]


plt.figure()
plt.errorbar(L, difference,yerr = difference_error)

plt.xlabel('System Size L')
plt.ylabel('Difference in average energy')
plt.title('Comparison energy of ECMC and MCMC')
plt.show()