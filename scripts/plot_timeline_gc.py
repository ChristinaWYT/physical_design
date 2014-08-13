import re
import matplotlib.pyplot as pyplot
import numpy as np
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-caseresult_dir", "--caseresult_dir", help="Result Dir")
parser.add_argument("-cases", "--cases", help="Cases")
parser.add_argument("-metric", "--metric", help="Metric")
#metric <- throughput, read_latency, write_latency
parser.add_argument("-workload", "--workload", help="Workload")
parser.add_argument("-title", "--title", help="Title")
parser.add_argument("-ylim", "--ylim", help="y-limit")
parser.add_argument("-plot_dir", "--plot_dir", help="Plot Directory")

args = parser.parse_args()

cases = args.cases.split(':')

c = ['b','r']
l = ['default', 'both compaction off']
#f, axarr = pyplot.subplots(len(cases), sharex=True, sharey=True)
lines=[]
count=-1
for case in cases:
	count=count+1
	time_instant=[]
	metric=[]
	with open(args.caseresult_dir + '/case' + case + '/slave1/hbase-hadoop-regionserver-sceplus-vm49.log') as file:
		for line in file:
			matchObj = re.match('.*: pause of approximately (\d+)ms.*', line)
			if matchObj:
				print('match')
				metric.append(int(matchObj.group(1)));
	p, = pyplot.plot(metric, color=c[count], label=l[count], linewidth=0.5)
	lines.append(p)
	pyplot.ylim([0,int(args.ylim)])
	#axarr[count].set_title(args.title)
	#axarr[count].set_ylim([0,50])

pyplot.ylabel("gc")
pyplot.xlabel("time")

#pyplot.legend([lines[0], lines[1]], ['Default','Both Compaction off'])	
#pyplot.show()
#pyplot.figure(2)
#pyplot.hist(metric, 100)
pyplot.savefig(args.plot_dir + args.workload + '_timeline_' + args.metric+ '_' + args.cases, bbox_inches='tight', pad_inches=0.2)
#pyplot.show()
