import re
import matplotlib.pyplot as pyplot
import numpy as np
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-result_dir", "--result_dir", help="Result Dir")
parser.add_argument("-result_file", "--result_file", help="Result File")
parser.add_argument("-metrics", "--metrics", help="Metrics")

args = parser.parse_args()

metrics = args.metrics.split(':')
d=dict()
for metric in metrics:
	d[metric]=[]

keys = d.keys();

with open(args.result_file , 'r') as file:
	for line in file:
		words=line.split()
		for word in words:
			kv = word.strip(',').split('=')
			if kv[0] in keys:
				l = d[kv[0]]
				l.append(kv[1])

color=['r', 'g', 'b', 'c', 'p', 'y']
pyplot.figure(1)

count=0
for k in keys:
	print(k, *d[k], sep=',', end='\n')
	pyplot.plot(d[k], color=color[count], marker='o', label= k)
	count=count+1

pyplot.legend()
pyplot.savefig(args.result_dir + 'io_metrics' + args.metrics + '.png')
pyplot.show()
