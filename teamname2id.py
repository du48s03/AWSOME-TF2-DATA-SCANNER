import sys
idmap = open(sys.argv[1],'r')
inputfile = open(sys.argv[2],'r')
outputfile = open(sys.argv[3], 'w')

name2id = {}
idmap.readline()
idmap.readline()
for line in idmap:
  line = line[:-1]
  if(len(line)==0):
    break;
  data = line.split(',')
  name2id[data[1]] = data[0]

print "Getting table schema"
table = inputfile.readline()[:-1];
attrs = inputfile.readline()[:-1].split(',');
print "attrs = ", attrs
loc= 0
for x in xrange(0,len(attrs)):
  if(attrs[x]=='team'):
    loc = x

print "loc = ",loc

print "writing output"
outputfile.write(table+"\n")
outputfile.write(','.join(attrs)+"\n")
for line in inputfile:
  line = line[:-1]
  if(len(line)==0):
    break
  data = line.split(',')
  data[loc] = name2id[data[loc]]
  outputfile.write(','.join(data)+"\n")
outputfile.write("\n")
      
