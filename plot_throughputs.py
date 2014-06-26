import matplotlib.pyplot as pyplot
import numpy as np
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-result_dir", "--result_dir", help="Result Dir")

args = parser.parse_args()

load_throughputs = []
rr_throughputs = []
scan_throughputs = []

for i in range(1,10):
	with open(args.result_dir + '/load_' + str(i) + '.dat', 'r') as file:
		for line in file:
			words = line.split()
			if len(words) == 3:
				if words[0] == '[OVERALL],' and words[1] == 'Throughput(ops/sec),':
					load_throughputs.append(words[2])

for i in range(1,10):
	with open(args.result_dir + '/random_read_' + str(i) + '.dat', 'r') as file:
		for line in file:
			words = line.split()
			if len(words) == 3:
				if words[0] == '[OVERALL],' and words[1] == 'Throughput(ops/sec),':
					rr_throughputs.append(words[2])
	

for i in range(1,10):
	with open(args.result_dir + '/scan_' + str(i) + '.dat', 'r') as file:
		for line in file:
			words = line.split()
			if len(words) == 3:
				if words[0] == '[OVERALL],' and words[1] == 'Throughput(ops/sec),':
					scan_throughputs.append(words[2])
	
print(*load_throughputs, sep=',', end='\n')
print(*rr_throughputs, sep=',', end='\n')
print(*scan_throughputs, sep=',', end='\n')

pyplot.plot(range(1,10), load_throughputs, color='r', marker='o', label="load")
pyplot.plot(range(1,10), rr_throughputs, color='b', marker='o', label="random read")
pyplot.plot(range(1,10), scan_throughputs, color='g', marker='o', label="scan")

pyplot.ylabel('Throughput')

pyplot.legend()
pyplot.axis([0,10, 0, 13000])
pyplot.xticks([1,2,3,4,5,6,7,8,9],['None', 'GZ', 'SNAPPY', 'PREFIX', 'PREFIX_TREE', 'DIFF', 'FAST_DIFF', 'ROW', 'ROWCOL' ], rotation=30)
pyplot.savefig(args.result_dir + '/throughputs.png')
pyplot.show()
