import re
import matplotlib.pyplot as pyplot
import numpy as np
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-caseresult_dir", "--caseresult_dir", help="Case Result Dir")
parser.add_argument("-cases", "--cases", help="Cases")
parser.add_argument("-metric", "--metric", help="Metric")
parser.add_argument("-workload", "--workload", help="Workload")
parser.add_argument("-title", "--title", help="Title")
parser.add_argument("-ylim_max", "--ylim_max", help="y-limit-max")
parser.add_argument("-ylim_min", "--ylim_min", help="y-limit-min")
parser.add_argument("-plot_dir", "--plot_dir", help="Plot Directory")
parser.add_argument("-metric_file", "--metric_file", help="metric file")

args = parser.parse_args()

def create_timeline(subdir):
	count=-1
	count=count+1
	metrics = []
	with open(args.caseresult_dir + '/case' + args.cases + subdir + '/' + args.metric_file , 'r') as file:
		for line in file:
			interesting = False
			words=line.split()
			for word in words:
				if word == 'hfile.LruBlockCache:':
					interesting = True
				if interesting == True:
					kv = word.strip(',').split('=')
					p = re.compile('max')	
					if p.match(kv[0]):
						print(kv[0])
						metrics.append(float(kv[1]))
	pyplot.title(args.title)
	pyplot.plot(metrics)
	print(*metrics, sep=',', end='\n')
	pyplot.ylim(float(args.ylim_min),float(args.ylim_max)) 
	pyplot.tight_layout();
	pyplot.savefig(args.plot_dir + args.workload + '__timeline_' + args.metric+ '_' + args.cases, bbox_inches='tight', pad_inches=0.2)

pyplot.figure(1)
create_timeline('/slave1')

