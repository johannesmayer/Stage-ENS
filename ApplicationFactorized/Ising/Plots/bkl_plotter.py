import numpy, matplotlib.pyplot as plt, sys

if len(sys.argv) != 4:
    sys.exit("######### WRONG INPUT ########### GIVE ME THE INPUT IN THE FOLLOWING ORDER: <standard-file from AnalysisData> _ <factorized file form AnalysisData> _ <Diagram Title involving the Temperature>")

stand_title = sys.argv[1]
fact_title = sys.argv[2]
diagram_title = sys.argv[3]

corr_stand = numpy.load("AnalysisData/"+stand_title)
corr_fact = numpy.load("AnalysisData/"+fact_title)

e_axis = corr_stand[0]
m_axis = corr_stand[0]

e_index = e_axis < 800 
m_index = m_axis < 800
    
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

ax1.set_title("BKL Energy Autocorrelator"+diagram_title)
ax1.set_xlabel("Running Time")
ax1.set_ylabel("Autocorrelator")
ax1.set_yscale('log')
ax1.legend(loc='lower left', shadow=True)

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.plot(m_act_axis,m_act_autocorrelator_stand,'gx-',label='Standard Data')
ax2.plot(m_act_axis,m_act_autocorrelator_fact,'r-',label='Factorized-Filter Data')

ax2.set_title("BKL Magnetisation Autocorrelator"+diagram_title)
ax2.set_xlabel("Running Time")
ax2.set_ylabel("Autocorrelator")
ax2.set_yscale('log')
ax2.legend(loc='lower left', shadow=True)


fig1.savefig("Images/plot_of_enecorr_fttc_beta"+diagram_title+".png")
fig2.savefig("Images/plot_of_magcorr_fttc_beta_"+diagram_title+".png")

plt.show()
