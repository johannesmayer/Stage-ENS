import matplotlib.pyplot as plt
import numpy

markov_energies = numpy.array([-326.49 ,-579.27 ,-904.48])
event_energies = numpy.array([-326.43, -579.55, -904.66])

difference = markov_energies - event_energies



markov_errors =numpy.array([0.16,0.22,0.30])
event_errors = numpy.array([0.11, 0.16, 0.20])

difference_error = numpy.sqrt(markov_errors**2 + event_errors**2)

L = [15, 20 ,25]


plt.figure()
plt.errorbar(L, difference,yerr = difference_error)

plt.xlabel('System Size L')
plt.ylabel('Difference in average energy')
plt.title('Comparison energy of ECMC and MCMC')
plt.show()