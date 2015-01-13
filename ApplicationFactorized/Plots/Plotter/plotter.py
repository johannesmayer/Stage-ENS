import numpy, matplotlib.pyplot as plt


correlation = numpy.load("/Users/johannesmayer/GitHub/Stage-ENS/ApplicationFactorized/DataAnalysis/correlation_standard_metrop.npy")

axis = correlation[0]
autocorrelator = correlation[1]

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.plot(axis,autocorrelator,'go')
#ax1.set_yscale('log')
fig1.show()