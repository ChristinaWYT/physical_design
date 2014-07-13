import re
import matplotlib.pyplot as pyplot
import numpy as np
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-caseresult_dir", "--caseresult_dir", help="Result Dir")
parser.add_argument("-cases", "--cases", help="Cases")
parser.add_argument("-metric", "--metric", help="Metric")
parser.add_argument("-workload", "--workload", help="Workload")

args = parser.parse_args()

cases = args.cases.split(':')

f, axarr = pyplot.subplots(len(cases), sharex=True, sharey=True)
count=-1
for case in cases:
	count=count+1
	time_instant=[]
	metric=[]
	with open(args.caseresult_dir + '/case' + case + '/case'+case+'.log') as file:
		for line in file:
			words = line.split()
			#print(words)
			if len(words) > 6:
			#print(words)
				if words[3]== 'sec:' and words[5] == 'operations;' and words[7]== 'current' and words[8] == 'ops/sec;':# and words[6] != '0':
					print(words[2] + " " + words[6])
					time_instant.append(int(words[2]))
					#throughputs.append(float(words[6]))
					if args.metric == 'throughput':
						metric.append(float(words[6]))
					elif args.metric == 'read_latency':
						metric.append(float(words[12].strip(']').split('=')[1]))
						#print(words[12].strip(']').split('=')[1])
					elif args.metric == 'write_latency':
						metric.append(float(words[10].strip(']').split('=')[1]))
						#print(words[10].strip(']').split('=')[1])
	axarr[count].scatter(time_instant, metric)
	axarr[count].set_ylim([0,50000])
	axarr[count].set_title('experiment ' + str(count+1))
	#axarr[count].set_ylim([0,50])
	
#pyplot.show()
#pyplot.figure(2)
#pyplot.hist(metric, 100)
pyplot.savefig(args.workload + '_timeline_' + args.metric+ '_' + args.cases, bbox_inches='tight', pad_inches=0.2)
#pyplot.show()
