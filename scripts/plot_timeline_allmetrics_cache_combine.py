import re
import matplotlib.pyplot as pyplot
import numpy as np
import argparse
parser = argparse.ArgumentParser()

c=['r','b','g', 'c', 'm','k','y']
#c=['r','b']
parser.add_argument("-caseresult_dir", "--caseresult_dir", help="Case Result Dir")
parser.add_argument("-cases", "--cases", help="Cases")
parser.add_argument("-metric", "--metric", help="Metric")
parser.add_argument("-workload", "--workload", help="Workload")
parser.add_argument("-title", "--title", help="Title")
parser.add_argument("-ylim_max", "--ylim_max", help="y-limit-max")
parser.add_argument("-ylim_min", "--ylim_min", help="y-limit-min")
parser.add_argument("-plot_dir", "--plot_dir", help="Plot Directory")
parser.add_argument("-plot_type", "--plot_type", help="Plot Type")
parser.add_argument("-metric_file", "--metric_file", help="metric file")

args = parser.parse_args()


cases =args.cases.split(':')


def create_timeline(subdir):
	count=-1
	for case in cases:
		count=count+1
		master_metrics = []
		slave1_metrics = []
		time_instant=[]
		with open(args.caseresult_dir + '/case' + case + subdir + '/' + args.metric_file , 'r') as file:
			for line in file:
				master_total_size=0
				slave1_total_size=0
				words=line.split()
				for word in words:
					kv = word.strip(',').split('=')
					p = re.compile('blockCacheFreeSize')
					if p.match(kv[0]):
						if subdir == '/master':
							master_total_size = master_total_size + float(kv[1]);
						elif subdir == '/slave1':
							slave1_total_size = slave1_total_size + float(kv[1]);
						time_instant.append(float(words[0]))
					p = re.compile('blockCacheSize')
					if p.match(kv[0]):
						if subdir == '/master':
							master_total_size = master_total_size + float(kv[1]);
						elif subdir == '/slave1':
							slave1_total_size = slave1_total_size + float(kv[1]);
						master_metrics.append(master_total_size/(1024*1024*1024))
						slave1_metrics.append(slave1_total_size/(1024*1024*1024))
		#axarr[count].set_title(args.title)
		if subdir == '/slave1':
			if args.plot_type == 'scatter':
				pyplot.plot(range(len(time_instant)), slave1_metrics, color=c[count])
			elif args.plot_type == 'hist':
				pyplot.hist(slave1_metrics, 10)
			print('printing slave1...')
			print(*slave1_metrics, sep=',', end='\n')
			pyplot.ylim(float(args.ylim_min),float(args.ylim_max)) 
	pyplot.savefig(args.plot_dir + args.workload + '_slave1_timeline_' + args.metric+ '_' + args.cases, bbox_inches='tight', pad_inches=0.2)


pyplot.figure(1)
create_timeline('/slave1')

