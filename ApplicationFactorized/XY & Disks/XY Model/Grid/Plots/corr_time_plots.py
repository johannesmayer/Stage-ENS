import matplotlib.pyplot as plt
import numpy

markov_times = numpy.array([4.8,5.1,5.4,5.7])
event_times = numpy.array([3.4,3.7,4.0,4.1])

ratio = markov_times / event_times

L = [10,15, 20 ,25]


plt.figure()
plt.plot(L,markov_times,'bo',label='MCMC')
plt.plot(L,event_times,'ro',label='ECMC')
plt.plot(L,ratio,'go',label='ratio')

plt.legend(loc='right center')

plt.xlabel('System Size L')
plt.ylabel('Correlation time')
plt.title('Comparitons between correlation times for ECMC and MCMC')
plt.show()
plt.savefig('corr_time_comp.png')