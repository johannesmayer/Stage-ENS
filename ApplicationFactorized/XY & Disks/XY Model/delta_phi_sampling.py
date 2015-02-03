import numpy, math, matplotlib.pyplot as plt


#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####

def whos_lift(my_data):
    lift = 0
    if my_data[0][0][0] == my_data[1][0][0]:
        lift = 1
    return lift
    
#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####+#####

twopi = 2*math.pi


data_step = 0.04 * math.pi
all_delta_phi = []

all_data = numpy.load("2 Particle Data/two_spins.npy")
markov_chain = numpy.load("2 Particle Data/markov_histogram.npy")

for i_sweep in range(len(all_data)):
    if i_sweep % 1000 == 0:
        print("PROGRESS: "+str(i_sweep)+"/"+str(len(all_data)))
    data = all_data[i_sweep]
    #print data
    lift = whos_lift(data)
    #print("LIFT: "+str(lift))
    rest = 0
    for index in range(len(data)-1):
        phi_still = data[index][0][(lift+1)%2]
        phi_move = data[index][0][lift]
        phi_to = data[index+1][0][lift]
        #print("Still "+str(phi_still))
        #print("REST: "+str(rest))
        if phi_to < phi_move:
            phi_to += twopi
        full_turns = data[index+1][1]
        #print("FULL TURNS: "+str(full_turns))
        phi_to = phi_to + twopi*full_turns
        if phi_move + rest > phi_to:
            rest = ((phi_move + rest) - phi_to)%twopi
            continue       
        else: 
            phi_move += rest
            
        #print("Move "+str(phi_move))
        #print("To "+str(phi_to))
        
        while phi_move < phi_to:
            #print (phi_move - phi_still)/math.pi
            if lift == 0:
                all_delta_phi.append((phi_move - phi_still)%twopi)
            elif lift == 1:
                all_delta_phi.append((-phi_move + phi_still)%twopi)
            
            if phi_move + data_step < phi_to:
                phi_move += data_step
                #print("PHI MOVE FREE: "+str(phi_move))

            else:
                remain = phi_to - phi_move
                rest = phi_move + data_step - phi_to
                
                phi_move += remain
                #print("PHI MOVE REST: "+str(phi_move))
                lift = (lift+1)%2
                
all_delta_phi = numpy.array(all_delta_phi)    
    


numpy.save("2 Particle Data/event_chain.npy",all_delta_phi)

                
                
                
                