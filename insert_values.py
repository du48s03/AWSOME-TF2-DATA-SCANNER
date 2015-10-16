#Read values from a file and generates the postgresql script for inserting those files
#The first line is the table name.
#The second line contains the attribute names, separated by commas. 
#The following lines contains the data, seperated by commas. 
import sys
import subprocess

infilename = sys.argv[1]
outfilename = sys.argv[2]

user = "lch2135"
host = "w4111db1.cloudapp.net"
db = "proj1part2"

f = open(infilename, 'r')
OUTPUT = open(outfilename, 'w')
tablename = f.readline()[:-1]
attrnames = f.readline()[:-1]
attrs = attrnames.split(',')
for line in f:
	if(len(line)==1):
		break;
	data = line[:-1].split(',')
	OUTPUT.write('INSERT INTO '+tablename+'(')
	for x in xrange(0, len(attrs)-1):
		OUTPUT.write(attrs[x]+',')
	OUTPUT.write(attrs[-1])
	OUTPUT.write(') VALUES(')
	for x in xrange(0, len(data)-1):
		OUTPUT.write(data[x]+',')
	OUTPUT.write(data[-1])
	OUTPUT.write(');\n')

#print subprocess.check_output(["psql", "-U", user, "-h", host, db, "-a", "-f", outfilename], stderr=subprocess.STDOUT)
