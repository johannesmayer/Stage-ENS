import numpy, matplotlib.pyplot as plt, sys


if len(sys.argv) != 3:
    sys.exit("GIVE ME THE DATA FILE AND THE THERMAL CUTOFF")
    
    
thermal_cutoff = int(sys.argv[2])
data = numpy.load(sys.argv[1])
data = data[1]
data = data[thermal_cutoff:]
fig, axes = plt.subplots(nrows=2, ncols=1)

ax1 = axes[0]
ax2 = axes[1]
ax1.plot(data)
ax2.hist(data, bins=100, normed=True)


plt.show()