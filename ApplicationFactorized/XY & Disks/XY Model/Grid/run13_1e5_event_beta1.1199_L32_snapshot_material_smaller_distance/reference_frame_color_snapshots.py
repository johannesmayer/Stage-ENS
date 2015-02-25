# date:   2014-10-09
# author: tc

import numpy
import random
import math
import cmath
import itertools
import pylab
import sys
import os
from matplotlib.colors import LinearSegmentedColormap

###############################################################################


def xy_magnetisation(spin_config):
    N = len(spin_config)
    if type(spin_config) != numpy.ndarray:
        spin_config = numpy.array(spin_config)
    mag = sum(numpy.exp(1j*spin_config))
    return mag/float(N)
    
def average_angle(spin_config):
    mag = xy_magnetisation(spin_config)/abs(xy_magnetisation(spin_config))
    phi = numpy.real((1/(1j)*numpy.log(mag)))%(2*math.pi)
    return (phi+math.pi)%(2*math.pi)

## PART 1 (not related to the animation)

# number of configurations:

if len(sys.argv) != 5:
    sys.exit("GIVE NAME OF CONFIGURATION LIST IN FOLDER GRID DATA : BETA : L : CLUSTER OR EVENT")

# linear size of the system:
L = int(sys.argv[3])
K = L*L
# get the list of configurations from somewhere, e.g. generate them randomly
#list_conf = [numpy.random.uniform(0.0, 2.0 * numpy.pi, size=(L, L)) for step in xrange(nsteps)]
my_data = numpy.load(sys.argv[1])
#my_data = numpy.load("Longruns/"+sys.argv[1])
list_conf = []
#for index in range(len(my_data[0])):
for config in my_data:
    config = (config - average_angle(config))%(2*math.pi)
    list_conf.append(config)
nsteps = len(list_conf)

###############################################################################

## PART 2 (not related to the animation)

list_L = range(L)
fig = pylab.figure()
outdir = 'color_snapshots'
filename = sys.argv[4]+'beta_'+sys.argv[2]+'_L_'+sys.argv[3]
filename = outdir+'/'+filename
if not os.path.isdir(outdir):
    os.makedirs(outdir)
    

startcolor = '#000000'
midcolor = '#ffffff'

cmap = LinearSegmentedColormap.from_list('BlackForth',[startcolor,midcolor,startcolor])



for step in xrange(nsteps):
    print step, nsteps
        
    ax = pylab.gca()
    ax.set_aspect(1)
    ax.xaxis.set_major_locator(pylab.NullLocator())
    ax.yaxis.set_major_locator(pylab.NullLocator())
    conf = list_conf[step]
    conf = numpy.reshape(conf,(L,L))
    pylab.axis([-0.5, L-0.5, -0.5, L - 0.5])
    var = pylab.imshow(conf,interpolation = 'nearest',vmin = 0, vmax = 2*math.pi,cmap = cmap)
    supe = pylab.colorbar(ticks=[0,math.pi,2*math.pi])
    supe.ax.set_yticklabels(['$-\pi$','0','$\pi$'])
    
    pylab.savefig(filename+'_snapshot_%06i.png' % step, bbox_inches='tight')
    
    pylab.clf()
