import re
import matplotlib.pyplot as pyplot
import numpy as np
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-result_dir", "--result_dir", help="Result Dir")
parser.add_argument("-metrics", "--metrics", help="Metrics")

args = parser.parse_args()

master_metrics = []
slave1_metrics = []

with open(args.result_dir + '/master/all.metrics' , 'r') as file:
	for line in file:
		count=0
		words=line.split()
		for word in words:
			kv = word.strip(',').split('=')
			p = re.compile(args.metrics)	
			if p.match(kv[0]):
				count = count + int(kv[1])
		if count != 0:
			master_metrics.append(count)

with open(args.result_dir + '/slave1/all.metrics' , 'r') as file:
	for line in file:
		count=0
		words=line.split()
		for word in words:
			kv = word.strip(',').split('=')
			p = re.compile(args.metrics)	
			if p.match(kv[0]):
				count = count + int(kv[1])
		if count != 0:
			slave1_metrics.append(count)

print('printing master...')
print(*master_metrics, sep=',', end='\n')
print('printing slave1...')
print(*slave1_metrics, sep=',', end='\n')

pyplot.figure(1)
pyplot.plot(master_metrics, color='r', marker='o', label="master " + args.metrics)
pyplot.savefig(args.result_dir + '/master_' + args.metrics + '.png')
pyplot.show()

pyplot.figure(2)
pyplot.plot(slave1_metrics, color='r', marker='o', label="slave1" + args.metrics)
pyplot.savefig(args.result_dir + '/slave1_compaction' + args.metrics  + '.png')
pyplot.show()
