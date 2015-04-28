# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt, math, numpy
from matplotlib.patches import FancyArrowPatch

pi = math.pi
L=2
lift = 0
fig = plt.gcf()
ax = plt.gca()
ax.set_aspect(1)

ax.xaxis.set_major_locator(plt.NullLocator())
ax.yaxis.set_major_locator(plt.NullLocator())

for dire in ['top','bottom','left','right']:
    ax.spines[dire].set_linewidth(4)

delta = pi/4.0
angles0 = []
angles1 = [pi,pi,pi,pi,pi,pi,pi,pi,pi]
angles2 = []


filename = 'conceptcurve'
plt.axis([0.0, 9, 0.0, 3.])
for index in range(9):
    if index not in [0,1,2,3,4,5,6,7,8]:
        phi = angles0[index]
        y = 0.5
        vz = 0.0
        if index in [0,3,6]:
            vz = 0.5
        if index in [2,5,8]:
            vz = -0.5
        x = index + vz + 0.5
        dx, dy = 0.6 * math.cos(phi) / 2.0, 0.6 * math.sin(phi) / 2.0

        x0, x1 = x - dx, x + dx
        y0, y1 = y - dy, y + dy
        col = 'k'
        if index in [2]:
            col = 'g'
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='Simple, head_width=15, head_length=10, tail_width = 5.0', fc=col, ec=col))
    else: ax.add_patch(FancyArrowPatch((0,3), (1,1), arrowstyle='Simple, head_width=0, head_length=0, tail_width = 0.0', fc='k', ec='k'))
    
for index in range(9):
    phi = angles1[index]
    y = 1.5
    vz = 0.0
    if index in [0,3,6]:
        vz = 0.4
    if index in [2,5,8]:
        vz = -0.4
    x = index + vz + 0.5
    dx, dy = 0.6 * math.cos(phi) / 2.0, 0.6 * math.sin(phi) / 2.0
    x0, x1 = x - dx, x + dx
    y0, y1 = y - dy, y + dy
    col = 'k'
    if index in [0,3,6]:
        col = 'g'
    if index in [1,4,7]:
        col = 'b'
    if index in [2,5,8]:
        col = 'r'
        
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='Simple, head_width=15, head_length=10, tail_width = 5.0', fc=col, ec=col))
    myaxis = numpy.linspace(-pi, pi, 100)
    ax.plot(myaxis, numpy.cos(myaxis))
    
    
for index in range(6):
    if index not in [0,1,2,3,4,5,6,7,8]:
        phi = angles2[index]
        y = 2.5
        vz = 0.0
        if index in [0,3,6]:
            vz = 0.5
        if index in [2,5,8]:
            vz = -0.5
        x = index + vz + 0.5
        dx, dy = 0.6 * math.cos(phi) / 2.0, 0.6 * math.sin(phi) / 2.0

        x0, x1 = x - dx, x + dx
        y0, y1 = y - dy, y + dy
        col = 'k'
        if index in [0,3,6]:
            col = 'g'
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='Simple, head_width=15, head_length=10, tail_width = 5.0', fc=col, ec=col))
    else: ax.add_patch(FancyArrowPatch((0,3), (1,1), arrowstyle='Simple, head_width=0, head_length=0, tail_width = 0.0', fc='k', ec='k'))


ax.annotate("",
            xy=(3.7, 1.5), xycoords='data',
            xytext=(2.5, 1.5), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3,rad=-0.0"), 
            )




plt.savefig('/Users/johannesmayer/Documents/Universität/ERASMUS/Stage/Python/Pythonplots/FürWerner/'+filename+'.pdf',format = 'pdf',dpi=fig.dpi,bbox_inches='tight')
plt.show()

