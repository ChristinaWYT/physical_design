import re
import matplotlib.pyplot as pyplot
import numpy as np
import argparse
from operator import add

def make_patch_spines_invisible(ax):
  ax.set_frame_on(True)
  ax.patch.set_visible(False)
    #for sp in ax.spines.itervalues():
    #    sp.set_visible(False)
  for k in ax.spines.keys():
        ax.spines[k].set_visible(False)

parser = argparse.ArgumentParser()

parser.add_argument("-caseresult_dir", "--caseresult_dir", help="Result Dir")
parser.add_argument("-cases", "--cases", help="Cases")
parser.add_argument("-title", "--title", help="Title")
parser.add_argument("-plot_dir", "--plot_dir", help="plot directory")
parser.add_argument("-workload", "--workload", help="Workload type")

args = parser.parse_args()

throughputs=[]
insert_latency=[]
read_latency=[]

cases = args.cases.split(':')

# collecting the workloadc throughputs
for case in cases:
	if args.workload == 'load':
		ycsb_log = args.caseresult_dir + '/case' + case + '/load_1.dat'
	elif args.workload == 'workloada':
		ycsb_log = args.caseresult_dir + '/case' + case + '/workloada_1.dat'
	elif args.workload == 'workloadb':
		ycsb_log = args.caseresult_dir + '/case' + case + '/workloadb_1.dat'
	elif args.workload == 'workloadc':
		ycsb_log = args.caseresult_dir + '/case' + case + '/workloadc_1.dat'

	with open(ycsb_log, 'r') as file:
		for line in file:
			words = line.split()
			if len(words) == 3:
				if words[0] == '[OVERALL],' and words[1] == 'Throughput(ops/sec),':
					throughputs.append(float(words[2]))
				if words[0] == '[INSERT],' and words[1] == 'AverageLatency(us),':
					insert_latency.append(float(words[2]))
				if words[0] == '[READ],' and words[1] == 'AverageLatency(us),':
					read_latency.append(float(words[2]))

print(*throughputs, sep=',', end='\n')
print(*insert_latency, sep=',', end='\n')
print(*read_latency, sep=',', end='\n')

fig, ax1 = pyplot.subplots()
fig.subplots_adjust(right=0.75)
p1, = ax1.plot([1,2,3], throughputs, color='r', marker='o', label= args.workload + " throughput", linewidth=1.5)
ax2 = ax1.twinx()
p2, = ax2.plot([1,2,3], insert_latency, color='b', marker='o', label= args.workload + " insert average latency", linewidth=1.5)

if args.workload == 'workloadc' or args.workload == 'workloadb' or args.workload == 'workloada':
	ax3 = ax1.twinx()
	p3, = ax3.plot([1,2,3], read_latency, color='g', marker='o', label=args.workload + " read average latency", linewidth=1.5)
	ax3.spines["right"].set_position(("axes", 1.2))
	make_patch_spines_invisible(ax3)
	ax3.spines["right"].set_visible(True)

ax1.yaxis.label.set_color(p1.get_color())
ax2.yaxis.label.set_color(p2.get_color())
if args.workload == 'workloadc':
	ax3.yaxis.label.set_color(p3.get_color())

ax1.set_ylabel('Throughput')
ax2.set_ylabel('Insert latency')
if args.workload == 'workloadc':
	ax3.set_ylabel('Read latency')

pyplot.xticks([1,2,3],['Default', 'Major Off', 'Major and Minor Off'], rotation=30)


tkw = dict(size=10, width=1.5)
ax1.tick_params(axis='y', colors=p1.get_color(), **tkw)
ax2.tick_params(axis='y', colors=p2.get_color(), **tkw)
if args.workload == 'workloadc':
	ax3.tick_params(axis='y', colors=p3.get_color(), **tkw)
ax1.tick_params(axis='x', **tkw)

if args.workload == 'workloadc':
	lines = [p1, p2, p3]
else:
	lines = [p1,p2]
ax1.legend(lines, [l.get_label() for l in lines])

pyplot.title(args.title)
pyplot.savefig(args.plot_dir + args.workload + '_latency_' + args.cases, bbox_inches='tight', pad_inches=0.2)
#pyplot.show()
