# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import math
import numpy
from matplotlib.patches import FancyArrowPatch, Ellipse


def potential(J,xaxis):
    return -J*numpy.cos(xaxis)


pi = math.pi


xaxis = numpy.linspace(-pi,pi,1000)

xTickpos = [-pi,-0.5*pi,0,0.5*pi,pi]
xLabels = ['$-\\pi$','$-\\frac{\\pi}{2}$','$0$','$\\frac{\\pi}{2}$','$\\pi$']


yTickpos = [-1,0,1]

yLabels12 = ['-$J_{12}$',0,'$J_{12}$']
yLabels23 = ['-$J_{23}$',0,'$J_{23}$']

emptyLabels = ['','','']

refX0, refX1, refY0, refY1 = 0,0,0,0

#### MAKE FIGURE #############################


##############################
ax = plt.subplot(3, 3, 1)


ax.plot(xaxis,potential(1,xaxis),'g',lw = '1')
ax.set_xlim(-pi,pi)
ax.set_ylim(-1.1,1.1)


ax.set_xticks(xTickpos)
ax.set_xticklabels(xLabels,size = 15)

ax.set_yticks(yTickpos)
ax.set_yticklabels(yLabels12, size = 10)

ax.set_ylabel('$E_{12}$',rotation = 'horizontal')
ax.set_xlabel('$\\Delta \\Phi _{12}$')



dx = 3.0
dy = 2*pi

maxd = max(dx, dy)
width = .15 * maxd / dx
height = .15 * maxd / dy

part_pos = Ellipse((-0.5*pi, 0.0), width, height,ec='k')
ax.add_patch(part_pos)


ax.annotate('',
            xy=(0.5*pi, -1.0), xycoords='data',
            xytext=(0.5*pi, 0.0), textcoords='data',
            arrowprops=dict(arrowstyle="-",ec='g',lw=2,
                            connectionstyle="arc"), 
            )

box = dict(boxstyle="square,pad=0.", fc="white", ec="k", lw=0)
ax.text(0.75*pi, -0.8 ,'$E^*_{12}$',ha="center", va="center", rotation=0,
            size=15,color='g',
            bbox=box)

#############################################################################
ax = plt.subplot(3, 3, 2)

ax.plot(xaxis,potential(1,xaxis),'g',lw = '1')
ax.set_xlim(-pi,pi)
ax.set_ylim(-1.1,1.1)


ax.set_xticks(xTickpos)
ax.set_xticklabels(xLabels,size = 15)

ax.set_yticks(yTickpos)
ax.set_yticklabels(emptyLabels, size = 10)

ax.set_xlabel('$\\Delta \\Phi _{12}$')

dx = 3.0
dy = 2*pi

maxd = max(dx, dy)
width = .15 * maxd / dx
height = .15 * maxd / dy

part_pos = Ellipse((0.0, -1.0), width, height,ec='k')
ax.add_patch(part_pos)

ax.annotate('',
            xy=(0.5*pi, -1.0), xycoords='data',
            xytext=(0.5*pi, 0.0), textcoords='data',
            arrowprops=dict(arrowstyle="-",ec='g',lw=2,
                            connectionstyle="arc"), 
            )

box = dict(boxstyle="square,pad=0.", fc="white", ec="k", lw=0)
ax.text(0.75*pi, -0.8 ,'$E^*_{12}$',ha="center", va="center", rotation=0,
            size=15,color='g',
            bbox=box)

#############################################################################
ax = plt.subplot(3, 3, 3)

ax.plot(xaxis,potential(1,xaxis),'g',lw = '1')
ax.set_xlim(-pi,pi)
ax.set_ylim(-1.1,1.1)


ax.set_xticks(xTickpos)
ax.set_xticklabels(xLabels,size = 15)

ax.set_yticks(yTickpos)
ax.set_yticklabels(emptyLabels, size = 10)

ax.set_xlabel('$\\Delta \\Phi _{12}$')

dx = 3.0
dy = 2*pi

maxd = max(dx, dy)
width = .15 * maxd / dx
height = .15 * maxd / dy

part_pos = Ellipse((0.25*pi, -1/math.sqrt(2)), width, height,ec='k')
ax.add_patch(part_pos)



ax.annotate('',
            xy=(0.5*pi, -1/math.sqrt(2)), xycoords='data',
            xytext=(0.5*pi, 0.), textcoords='data',
            arrowprops=dict(arrowstyle="-",ec='g',lw=2,
                            connectionstyle="arc"), 
            )
            
ax.annotate('',
            xy=(0.5*pi, -1.0), xycoords='data',
            xytext=(0.5*pi, -0.25), textcoords='data',
            arrowprops=dict(arrowstyle="-",ec='g',alpha = 0.3,lw=2,
                            connectionstyle="arc"), 
            )

box = dict(boxstyle="square,pad=0.", fc="white", ec="k", lw=0)
ax.text(0.75*pi, -0.8 ,'$E^*_{12}$',ha="center", va="center", rotation=0,
            size=15,color='g',
            bbox=box)

#############################################################################
ax = plt.subplot(3, 3, 4)
ax.axis('off')
angles0 = [pi,0.5*pi,0.5*pi]

for index in range(3):
    phi = angles0[index]
    
    y = 0.6
    vz = 0.0
    if index in [0]:
        vz = 0.2
    if index in [2]:
        vz = -0.2
    x = index/2.0 + vz 
    dx, dy = 0.6 * math.cos(phi) / 4., 0.6 * math.sin(phi) / 4.
    x0, x1 = x - dx, x + dx
    y0, y1 = y - dy, y + dy
    col = 'k'
    if index in [0]:
        col = 'g'
    if index in [1]:
        col = 'b'
    if index in [2]:
        col = 'r'
    if index == 1:
        refX0, refX1 = x0, x1
        refY0, refY1 = y0, y1
        
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='Simple, head_width=6, head_length=6, tail_width = 2', fc=col, ec=col))
    
    
ax.annotate('',
        xy=(1., 0.25), xycoords='data',
        xytext=(0., 0.25), textcoords='data',
        arrowprops=dict(arrowstyle="-",ec='b',lw=4,
                        connectionstyle="arc"), 
        )

box = dict(boxstyle="square,pad=0.", fc="white", ec="k", lw=0)
ax.text(0.5, 0.05 ,'$\ell$',ha="center", va="center", rotation=0,
            size=25,color='b',
            bbox=box)

#############################################################################
ax = plt.subplot(3, 3, 5)
ax.axis('off')

angles1 = [pi,pi,0.5*pi]

for index in range(3):
    phi = angles1[index]
    y = 0.6
    vz = 0.0
    if index in [0]:
        vz = 0.2
    if index in [2]:
        vz = -0.2
    x = index/2.0 + vz 
    dx, dy = 0.6 * math.cos(phi) / 4., 0.6 * math.sin(phi) / 4.
    x0, x1 = x - dx, x + dx
    y0, y1 = y - dy, y + dy
    col = 'k'
    if index in [0]:
        col = 'g'
    if index in [1]:
        col = 'b'
    if index in [2]:
        col = 'r'
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='Simple, head_width=6, head_length=6, tail_width = 2', fc=col, ec=col))
    if index == 1 :
        ax.add_patch(FancyArrowPatch((refX0, refY0), (refX1, refY1), arrowstyle='Simple, head_width=6, head_length=6, tail_width = 2',alpha = 0.3, fc=col, ec=col))

    box = dict(boxstyle="square,pad=0.", fc="white", ec="k", lw=0)
    ax.text(x, 0.35 ,str(index+1),ha="center", va="center", rotation=0,
            size=15,color='k',
            bbox=box)

ax.annotate('',
        xy=(1., 0.22), xycoords='data',
        xytext=(0.4, 0.22), textcoords='data',
        arrowprops=dict(arrowstyle="-",ec='b',lw=4,
                        connectionstyle="arc"), 
        )
ax.annotate('',
        xy=(0.6, 0.22), xycoords='data',
        xytext=(0.0, 0.22), textcoords='data',
        arrowprops=dict(arrowstyle="-",ec='b',alpha = 0.3,lw=4,
                        connectionstyle="arc"), 
        )

box = dict(boxstyle="square,pad=0.", fc="white", ec="k", lw=0)
ax.text(0.5, 0.05 ,'$\ell$',ha="center", va="center", rotation=0,
            size=25,color='b',
            bbox=box)

#############################################################################
ax = plt.subplot(3, 3, 6)
ax.axis('off')

angles2 = [pi,1.25*pi,0.5*pi]

for index in range(3):
    phi = angles2[index]
    y = 0.6
    vz = 0.0
    if index in [0]:
        vz = 0.2
    if index in [2]:
        vz = -0.2
    x = index/2.0 + vz 
    dx, dy = 0.6 * math.cos(phi) / 4., 0.6 * math.sin(phi) / 4.
    x0, x1 = x - dx, x + dx
    y0, y1 = y - dy, y + dy
    col = 'k'
    if index in [0]:
        col = 'g'
    if index in [1]:
        col = 'b'
    if index in [2]:
        col = 'r'
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='Simple, head_width=6, head_length=6, tail_width = 2', fc=col, ec=col))
    if index == 1 :
        ax.add_patch(FancyArrowPatch((refX0, refY0), (refX1, refY1), arrowstyle='Simple, head_width=6, head_length=6, tail_width = 2',alpha = 0.3, fc=col, ec=col))

    
ax.annotate('',
        xy=(1., 0.25), xycoords='data',
        xytext=(0.6, 0.25), textcoords='data',
        arrowprops=dict(arrowstyle="-",ec='b',lw=4,
                        connectionstyle="arc"), 
        )
ax.annotate('',
        xy=(0.8, 0.25), xycoords='data',
        xytext=(0.0, 0.25), textcoords='data',
        arrowprops=dict(arrowstyle="-",ec='b',alpha = 0.3,lw=4,
                        connectionstyle="arc"), 
        )

box = dict(boxstyle="square,pad=0.", fc="white", ec="k", lw=0)
ax.text(0.5, 0.05 ,'$\ell$',ha="center", va="center", rotation=0,
            size=25,color='b',
            bbox=box)



#############################################################################
ax = plt.subplot(3, 3, 7)
ax.plot(xaxis,potential(1,xaxis),'r',lw = '1')
ax.set_xlim(-pi,pi)
ax.set_ylim(-1.1,1.1)



ax.set_xticks(xTickpos)
ax.set_xticklabels(xLabels,size = 15)

ax.set_yticks(yTickpos)
ax.set_yticklabels(yLabels23, size = 10)

ax.set_ylabel('$E_{23}$',rotation = 'horizontal')
ax.set_xlabel('$\\Delta \\Phi _{23}$')


part_pos = Ellipse((0.0, -1.0), width, height,ec='k')
ax.add_patch(part_pos)


ax.annotate('',
            xy=(0.75*pi, -1.0), xycoords='data',
            xytext=(0.75*pi, 1.0/(math.sqrt(2))), textcoords='data',
            arrowprops=dict(arrowstyle="-",ec='r',lw=2,
                            connectionstyle="arc"), 
            )

box = dict(boxstyle="square,pad=0.", fc="white", ec="k", lw=0)
ax.text(0.5*pi, -0.8 ,'$E^*_{23}$',ha="center", va="center", rotation=0,
            size=15,color='r',
            bbox=box)
            
            

#############################################################################
ax = plt.subplot(3, 3, 8)
ax.plot(xaxis,potential(1,xaxis),'r',lw = '1')
ax.set_xlim(-pi,pi)
ax.set_ylim(-1.1,1.1)


ax.set_xticks(xTickpos)
ax.set_xticklabels(xLabels,size = 15)
ax.set_yticks(yTickpos)
ax.set_yticklabels(emptyLabels, size = 10)

ax.set_xlabel('$\\Delta \\Phi _{23}$')


part_pos = Ellipse((0.5*pi, 0.0), width, height,ec='k')
ax.add_patch(part_pos)


ax.annotate('',
            xy=(0.75*pi, -1.0), xycoords='data',
            xytext=(0.75*pi, 0.2), textcoords='data',
            arrowprops=dict(arrowstyle="-",ec='r',alpha = 0.3,lw=2,
                            connectionstyle="arc"), 
            )
ax.annotate('',
            xy=(0.75*pi, 0.0), xycoords='data',
            xytext=(0.75*pi, 1.0/(math.sqrt(2))), textcoords='data',
            arrowprops=dict(arrowstyle="-",ec='r',lw=2,
                            connectionstyle="arc"), 
            )

box = dict(boxstyle="square,pad=0.", fc="white", ec="k", lw=0)
ax.text(0.5*pi, -0.8 ,'$E^*_{23}$',ha="center", va="center", rotation=0,
            size=15,color='r',
            bbox=box)

#############################################################################
ax = plt.subplot(3, 3, 9)
ax.plot(xaxis,potential(1,xaxis),'r',lw = '1')
ax.set_xlim(-pi,pi)
ax.set_ylim(-1.1,1.1)



ax.set_xticks(xTickpos)
ax.set_xticklabels(xLabels,size = 15)
ax.set_yticks(yTickpos)
ax.set_yticklabels(emptyLabels, size = 10)

ax.set_xlabel('$\\Delta \\Phi _{23}$')

ax.annotate('',
            xy=(0.75*pi, -1.0), xycoords='data',
            xytext=(0.75*pi, 1.0/(math.sqrt(2))), textcoords='data',
            arrowprops=dict(arrowstyle="-",ec='r',alpha = 0.3,lw=2,
                            connectionstyle="arc"), 
            )
dx = 3.0
dy = 2*pi

maxd = max(dx, dy)
width = .15 * maxd / dx
height = .15 * maxd / dy

part_pos = Ellipse((0.75*pi, 1/math.sqrt(2)), width, height,ec='k')
ax.add_patch(part_pos)


box = dict(boxstyle="square,pad=0.", fc="white", ec="k", lw=0)
ax.text(0.5*pi, -0.8 ,'$E^*_{23}$',ha="center", va="center", rotation=0,
            size=15,color='r',
            bbox=box)


#############################################################################
filename = 'concept_joh'
fig = plt.gcf()
plt.savefig('/Users/johannesmayer/Documents/Universität/ERASMUS/Stage/Python/Pythonplots/FürWerner/'+filename+'.pdf',format = 'pdf',dpi=fig.dpi,bbox_inches='tight')

plt.show()


