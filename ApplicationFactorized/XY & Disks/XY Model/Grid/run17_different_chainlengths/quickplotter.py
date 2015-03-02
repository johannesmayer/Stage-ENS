import numpy, matplotlib.pyplot as plt, sys


if len(sys.argv) != 3:
    sys.exit("GIVE ME THE DATA FILE AND THE THERMAL CUTOFF")
data = numpy.load(sys.argv[1])[int(sys.argv[2]):]





fig, axes = plt.subplots(nrows=2, ncols=1)

ax1 = axes[0]
ax2 = axes[1]

ax1.plot(data)
ax2.hist(data, bins=100, normed=True)


plt.show()