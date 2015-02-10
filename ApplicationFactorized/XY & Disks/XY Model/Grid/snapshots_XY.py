# date:   2014-10-09
# author: tc

import numpy
import random
import math
import itertools
import pylab
from matplotlib.patches import FancyArrowPatch
from matplotlib import animation

###############################################################################


## PART 1 (not related to the animation)

# number of configurations:


# linear size of the system:
L = 8
K = L*L
# get the list of configurations from somewhere, e.g. generate them randomly
#list_conf = [numpy.random.uniform(0.0, 2.0 * numpy.pi, size=(L, L)) for step in xrange(nsteps)]
my_data = numpy.load("Grid Data/xy_grid.npy")
list_conf = []
for index in range(len(my_data[0])):
    list_conf.append(my_data[0][index][0])
nsteps = len(list_conf)

###############################################################################

## PART 2 (not related to the animation)

list_L = range(L)
fig = pylab.figure()

for step in xrange(nsteps):
    print step, nsteps
    ax = pylab.gca()
    ax.set_aspect(1)
    ax.xaxis.set_major_locator(pylab.NullLocator())
    ax.yaxis.set_major_locator(pylab.NullLocator())
    conf = list_conf[step]
    pylab.axis([0.0, L, 0.0, L])
    [ax.axhline(y=i, ls='--', c='.7') for i in list_L]
    [ax.axvline(x=j, ls='--', c='.7') for j in list_L]
    patches = []
    for site in range(K):
        y = site // L
        x = site - y*L
        xc, yc = x + 0.5, y + 0.5
        theta = conf[site]
        dx, dy = 0.6 * math.cos(theta) / 2.0, 0.6 * math.sin(theta) / 2.0
        x0, x1 = xc - dx, xc + dx
        y0, y1 = yc - dy, yc + dy
        patches.append(ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='Simple, head_width=5, head_length=10', fc='k')))
    pylab.savefig('snapshot_%06i.png' % step, bbox_inches='tight')
    pylab.clf()
