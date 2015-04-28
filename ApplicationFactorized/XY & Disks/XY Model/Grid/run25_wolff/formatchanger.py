import numpy, sys, os


inputfile = sys.argv[1]
outdir = 'angular_clusterdata'
if not os.path.isdir(outdir):
    os.makedirs(outdir)
outputfile = 'angular_data_'+inputfile.split('/')[1]        
outputfile = outdir+'/'+outputfile
data = numpy.load(inputfile)
print numpy.shape(data)
convToangles = []
for spin in data:
    convToangles.append(numpy.arctan(spin[1]/spin[0]))
print numpy.shape(convToangles)
numpy.save(outputfile+'.npy', convToangles)