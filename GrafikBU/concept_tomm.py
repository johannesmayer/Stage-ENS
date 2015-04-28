# -*- coding: utf-8 -*-
from matplotlib import pyplot as pl
import math
import numpy

def add_line(start, end, ax, LW=1, LS='-'):
    ax.plot([start[0], end[0]], [start[1], end[1]], ls=LS, lw=LW, c='k')
    return




LW_bold = 3.5

## PLOT 1 #####################################################################
ax = pl.subplot(2, 1, 1)

delta = 0.2
dx = 2.0
for j in [1, 3, 5, 7]:
    add_line((dx * (j)     - delta, 0), (dx * (j + 1) + delta, 1), ax)
    add_line((dx * (j + 1) - delta, 1), (dx * (j + 2) + delta, 0), ax)
add_line((11, -0.55), (14, 0.7), ax)

x0, y0 = 4, -0.45
for (x0, y0) in [(3.5, -0.5), (4.0, -0.45)]:
    l = 1.7
    theta = 140 * math.pi / 180.0
    x1, y1 = x0 + l * math.cos(theta), y0 +l * math.sin(theta)
    add_line((x0, y0), (x1, y1), ax, LW=LW_bold)

ax.text(2.8, -0.45, '$s$', fontsize=18)
ax.text(4.0, -0.35, '$P$', fontsize=18)

ax.set_xlim(1.8, 19.5)
ax.set_ylim(-0.7, 1)

ax.set_aspect(2)

ax.axis('off')


## PLOT 2 #####################################################################
ax = pl.subplot(2, 2, 3)
for x in [3.85, 4.6, 9.5, 10.2]:
    add_line((x, 0), (x, 0.8), ax)

delta = 0.6
dx = 2
y = 0.3
add_line((dx * 2 - delta, y), (dx * 3 + delta, 0), ax)
add_line((dx * 3 - delta, 0),   (dx * 4 + delta, y), ax)
add_line((dx * 4 - delta, y), (dx * 5 + delta, 0), ax)
y = 0.6
ddx = 1.7
x = 4.2
add_line((x - ddx, y), (x, y), ax, LW=LW_bold)
x = 9.9
add_line((x + ddx, y), (x, y), ax, LW=LW_bold)

ax.text(2.8,  0.65, '$s$', fontsize=18)
ax.text(10.5, 0.65, '$P$', fontsize=18)

ax.set_aspect(5)

ax.axis('off')

## PLOT 3 #####################################################################
ax = pl.subplot(2, 4, 7)

l = 0.2
add_line((+l / 2.0, 0), (-0.5 - l / 2.0, - (1.0 + l) * math.sqrt(3.0) / 2.0), ax)
add_line((-l / 2.0, 0), (+0.5 + l / 2.0, - (1.0 + l) * math.sqrt(3.0) / 2.0), ax)
add_line((-0.5 - l, -math.sqrt(3.0) / 2.0), (0.5 + l, -math.sqrt(3.0) / 2.0), ax)
add_line((-0.2, -1.5), (-0.2, -0.7), ax, LW=LW_bold)
add_line((0.1, -0.5), (0.6, -0.1), ax, LW=LW_bold)
ax.text(-0.15, -1.4, '$s$', fontsize=18)
ax.text(0.3, -0.1, '$P$', fontsize=18)
ax.set_xlim(-0.5 -l, 0.5 + l)
ax.set_aspect(1)
ax.axis('off')

## PLOT 4 #####################################################################
ax = pl.subplot(2, 4, 8)
y = numpy.linspace(-1, 1, 100)
xl = y ** 2
xr = 1 - y ** 2
ax.plot(xl, y, 'k')
ax.plot(xr, y, 'k')
dx = 0.8
add_line((    - dx, 0), (      0.15, 0), ax, LW=LW_bold)
add_line((1.0 + dx, 0), (1.0 - 0.15, 0), ax, LW=LW_bold)
ax.set_xlim(- dx, 2 + dx)
ax.text(    - 0.6, 0.1, '$s$', fontsize=18)
ax.text(1.0 + 0.4, 0.1, '$P$', fontsize=18)
ax.set_aspect(1.7)
ax.axis('off')

###############################################################################

pl.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=-0.55)
pl.savefig('/Users/johannesmayer/Documents/Universität/ERASMUS/Stage/Python/Pythonplots/FürWerner/fig_nosezione.pdf', bbox_inches='tight')
pl.show()