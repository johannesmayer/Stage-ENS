import numpy, sys, math


################################################################################


def autocorrelation(my_list, delta):
    mean = numpy.mean(my_list[delta:]*my_list[:-delta])
    return mean
    
    
    
    
################################################################################

if len(sys.argv) != 4:
    sys.exit("++++++++################ GIVE ME THE INPUT IN THE FOLLOWING ORDER: DATA : THERMAL CUTOFF : UPPER LIMIT FOR SUMMING CORRELATION ################+++++++++++++++")

event_data = numpy.load(sys.argv[1])     
event_thermal_cutoff = int(sys.argv[2])
sum_to = int(sys.argv[3])


J = 1.
delta_max = 250
stepsize = 1

event_observable = []
event_correlator = []

all_deltas = []


event_observable = event_data[event_thermal_cutoff:]
  
print 'avg value ', numpy.mean(event_observable)
                       
event_observable = numpy.array(event_observable)

event_mean = numpy.mean(event_observable)
event_sq_expect = numpy.mean(event_observable*event_observable)

all_deltas = [0]
event_correlator = [1]

for delta in xrange(1,delta_max,stepsize):
    print delta, delta_max
    all_deltas.append(delta)
    event_correlator.append((autocorrelation(event_observable,delta)-event_mean**2)/(event_sq_expect - event_mean**2))


the_error = math.sqrt(( event_sq_expect - event_mean ** 2 ) / len(event_data)) * math.sqrt(event_correlator[0]+ 2*sum(event_correlator[1:sum_to]))


print 'ERROR',the_error