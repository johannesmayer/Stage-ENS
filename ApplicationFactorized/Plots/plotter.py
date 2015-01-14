import numpy, matplotlib.pyplot as plt


corr_stand = numpy.load("/Users/johannesmayer/GitHub/Stage-ENS/ApplicationFactorized/DataAnalysis/correlation_stand_metrop.npy")
corr_fact = numpy.load("/Users/johannesmayer/GitHub/Stage-ENS/ApplicationFactorized/DataAnalysis/correlation_fact_metrop.npy")

"""
corr_stand = numpy.load("/Users/johannesmayer/GitHub/Stage-ENS/ApplicationFactorized/DataAnalysis/correlation_stand_cluster.npy")
corr_fact = numpy.load("/Users/johannesmayer/GitHub/Stage-ENS/ApplicationFactorized/DataAnalysis/correlation_fact_cluster.npy")
"""



axis = corr_stand[0]
index = axis < 2500
print axis
act_axis = axis[index]

autocorrelator_stand = corr_stand[1]
act_autocorrelator_stand = autocorrelator_stand[index]
autocorrelator_fact = corr_fact[1]
act_autocorrelator_fact = autocorrelator_fact[index]



fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.plot(act_axis,act_autocorrelator_stand,'g-',label='Standard Data')
ax1.plot(act_axis,act_autocorrelator_fact,'r-',label='Factorized Filter Data')

ax1.set_title("Autocorrelation Functions for the energy at critical Temperature")
ax1.set_xlabel("Attempted Flips")
ax1.set_ylabel("Autocorrelator")
ax1.set_yscale('log')
ax1.legend(loc='lower left', shadow=True)
fig1.show()