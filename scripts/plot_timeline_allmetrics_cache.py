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
parser.add_argument("-plot_type", "--plot_type", help="Plot Type")
parser.add_argument("-metric_file", "--metric_file", help="metric file")

args = parser.parse_args()


cases =args.cases.split(':')


def create_timeline(subdir, axarr):
	count=-1
	for case in cases:
		count=count+1
		master_metrics = []
		slave1_metrics = []
		time_instant=[]
		with open(args.caseresult_dir + '/case' + case + subdir + '/' + args.metric_file , 'r') as file:
			for line in file:
				words=line.split()
				for word in words:
					kv = word.strip(',').split('=')
					p = re.compile(args.metric)	
					if p.match(kv[0]):
						print(kv[0])
						if subdir == '/master':
							print(kv[1])
							master_metrics.append(float(kv[1]))
						elif subdir == '/slave1':
							print(kv[1])
							slave1_metrics.append(float(kv[1]))
						time_instant.append(float(words[0]))

		if subdir == '/master':
			if args.plot_type == 'scatter':
				axarr[count].scatter(time_instant, master_metrics)
			elif args.plot_type == 'hist':
				axarr[count].hist(master_metrics, 10)
			print('printing master...')
			print(*master_metrics, sep=',', end='\n')
			pyplot.ylim(float(args.ylim_min),float(args.ylim_max)) 
			pyplot.tight_layout();
			pyplot.savefig(args.plot_dir + args.workload + '_master_timeline_' + args.metric+ '_' + args.cases, bbox_inches='tight', pad_inches=0.2)
		elif subdir == '/slave1':
			if args.plot_type == 'scatter':
				axarr[count].scatter(time_instant, slave1_metrics)
			elif args.plot_type == 'hist':
				axarr[count].hist(slave1_metrics, 10)
			print('printing slave1...')
			print(*slave1_metrics, sep=',', end='\n')
			pyplot.ylim(float(args.ylim_min),float(args.ylim_max)) 
			pyplot.tight_layout()
			pyplot.savefig(args.plot_dir + args.workload + '_slave1_timeline_' + args.metric+ '_' + args.cases, bbox_inches='tight', pad_inches=0.2)


pyplot.figure(1)
f1, axarr1 = pyplot.subplots(len(cases), sharey=True)
create_timeline('/master', axarr1)

pyplot.figure(2)
f2, axarr2 = pyplot.subplots(len(cases), sharey=True)
create_timeline('/slave1', axarr2)

