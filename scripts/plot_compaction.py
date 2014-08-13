import re
import matplotlib.pyplot as pyplot
import numpy as np
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-result_dir", "--result_dir", help="Result Dir")

args = parser.parse_args()

master_number_compaction = []
slave1_number_compaction = []

with open(args.result_dir + '/master/all.metrics' , 'r') as file:
	for line in file:
		count=0
		words=line.split()
		for word in words:
			kv = word.strip(',').split('=')
			p = re.compile('namespace_default_table_usertable_region_\w*_metric_numFilesCompactedCount')	
			if p.match(kv[0]):
				count = count + int(kv[1])
		if count != 0:
			master_number_compaction.append(count)

with open(args.result_dir + '/slave1/all.metrics' , 'r') as file:
	for line in file:
		count=0
		words=line.split()
		for word in words:
			kv = word.strip(',').split('=')
			p = re.compile('namespace_default_table_usertable_region_\w*_metric_numFilesCompactedCount')	
			if p.match(kv[0]):
				count = count + int(kv[1])
		if count != 0:
			slave1_number_compaction.append(count)

print('printing master...')
print(*master_number_compaction, sep=',', end='\n')
print('printing slave1...')
print(*slave1_number_compaction, sep=',', end='\n')

pyplot.figure(1)
pyplot.plot(master_number_compaction, color='r', marker='o', label="number of compaction in master")
pyplot.savefig(args.result_dir + '/master_compaction.png')
pyplot.show()

pyplot.figure(2)
pyplot.plot(slave1_number_compaction, color='r', marker='o', label="number of compaction in slave1")
pyplot.savefig(args.result_dir + '/slave1_compaction.png')
pyplot.show()
