import numpy, matplotlib.pylab as plt, sys


if len(sys.argv) != 7:
    sys.exit('GIVE ME INPUT IN THE FORM: PLUS FILE : MINUS FILE : ZERO FILE : PLUS THERM CUTOFF : MINUS THERM CUTOFF : ZERO THERM CUTOFF')    
    
    
    
therm_plus_cut = int(sys.argv[4])
therm_minus_cut = int(sys.argv[5])
therm_zero_cut = int(sys.argv[6])

plus = numpy.load("Grid_Data/"+sys.argv[1])[therm_plus_cut:]
minus = numpy.load("Grid_Data/"+sys.argv[2])[therm_minus_cut:]
zero = numpy.load("Grid_Data/"+sys.argv[3])[therm_zero_cut:]
print 'a'

plus_hist = plt.hist(plus, 100, normed= True, alpha=0.5, label='PLUS data',histtype = 'step')
minus_hist = plt.hist(minus, 100,normed=True, alpha = 0.5, label='MINUS data',histtype = 'step' )
zero_hist = plt.hist(zero, 100,normed=True, alpha = 0.5, label='ZERO data',histtype = 'step')

plt.title("Magnetic susceptibility histogram")
plt.xlabel('Magnetic susceptibility')
plt.ylabel('Frequency')

plt.legend(loc = 'upper left')

plt.show()