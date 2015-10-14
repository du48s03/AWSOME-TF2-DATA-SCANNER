#Read values from a file and generates the postgresql script for inserting those files
#The first line is the table name.
#The second line contains the attribute names, separated by commas. 
#The following lines contains the data, seperated by commas. 
import sys

infilename = sys.argv[1]
outfilename = sys.argv[2]
f = open(infilename, 'r')
OUTPUT = open(outfilename, 'w')
tablename = f.readline()[:-1]
attrnames = f.readline()[:-1]
attrs = attrnames.split(',')
print(attrs)
for line in f:
	data = line[:-1].split(',')
	OUTPUT.write('INSERT INTO '+tablename+'(')
	for x in xrange(0, len(attrs)-1):
		OUTPUT.write(attrs[x]+',')
	OUTPUT.write(attrs[-1])
	OUTPUT.write(') VALUES(')
	for x in xrange(0, len(data)):
		OUTPUT.write(data[x]+',')
	OUTPUT.write(data[-1])
	OUTPUT.write(');\n')


