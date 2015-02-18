import matplotlib.pyplot as plt
import numpy

event_mag = numpy.array([0.581,0.494,0.4477])
markov_mag = numpy.array([0.575,0.500,0.4471])

difference = markov_mag - event_mag

markov_errors =numpy.array([0.0023, 0.004, 0.0048])
event_errors = numpy.array([0.001, 0.002, 0.003])

difference_error = numpy.sqrt(markov_errors**2 + event_errors**2)

L = [10, 20 ,30]


plt.figure()
plt.errorbar(L, difference,yerr = difference_error)

plt.xlim(min(L)-5, max(L)+5)

plt.xlabel('System Size L')
plt.ylabel('Difference in average susceptibility')
plt.title('Comparison susceptibilty of ECMC and MCMC')
plt.show()