# -*- coding: utf-8 -*-
import numpy, matplotlib.pyplot as plt, sys

is_cluster = sys.argv[1]

if is_cluster == "Clusterplot":
    is_cluster = True
if is_cluster == "Localplot":
    is_cluster = False


if is_cluster ==True:
    isitcluster = "cluster"
else:
    isitcluster = "local"
    
    
stand_title = sys.argv[2]
fact_title = sys.argv[3]

#standard to first argument and factorized to 2nd one 
corr_stand = numpy.load("AnalysisData/"+stand_title)
corr_fact = numpy.load("AnalysisData/"+fact_title)


e_axis = corr_stand[0]
m_axis = corr_stand[0]


if is_cluster == True:
    e_index = e_axis < 100
    m_index = m_axis < 100
else:
    e_index = e_axis < 300
    m_index = m_axis < 300
    
e_act_axis = e_axis[e_index]
m_act_axis = m_axis[m_index]


e_autocorrelator_stand = corr_stand[1]
e_act_autocorrelator_stand = e_autocorrelator_stand[e_index]

e_autocorrelator_fact = corr_fact[1]
e_act_autocorrelator_fact = e_autocorrelator_fact[e_index]


m_autocorrelator_stand = corr_stand[2]
m_act_autocorrelator_stand = m_autocorrelator_stand[m_index]

m_autocorrelator_fact = corr_fact[2]
m_act_autocorrelator_fact = m_autocorrelator_fact[m_index]


fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.plot(e_act_axis,e_act_autocorrelator_stand,'gx-',label='Standard Data')
ax1.plot(e_act_axis,e_act_autocorrelator_fact,'r-',label='Factorized-Filter Data')

ax1.set_title("Plot of ene autocorr. for "+stand_title)
ax1.set_xlabel("Attempted "+isitcluster+" Flips")
ax1.set_ylabel("Autocorrelator")
ax1.set_yscale('log')
ax1.legend(loc='lower left', shadow=True)
#fig1.show()

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.plot(m_act_axis,m_act_autocorrelator_stand,'gx-',label='Standard Data')
ax2.plot(m_act_axis,m_act_autocorrelator_fact,'r-',label='Factorized-Filter Data')

ax2.set_title("Plot of mag autocorr. for "+stand_title)
ax2.set_xlabel("Attempted "+isitcluster+" Flips")
ax2.set_ylabel("Autocorrelator")
ax2.set_yscale('log')
ax2.legend(loc='lower left', shadow=True)


fig1.savefig("Images/plot_of_enecorr"+stand_title[:-4]+".png")
fig2.savefig("Images/plot_of_magcorr"+stand_title[:-4]+".png")

plt.show()




