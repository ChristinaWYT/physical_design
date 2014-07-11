import re
import matplotlib.pyplot as pyplot
import numpy as np
import argparse
from operator import add

import matplotlib

parser = argparse.ArgumentParser()

parser.add_argument("-caseresult_dir", "--caseresult_dir", help="Result Dir")
parser.add_argument("-cases", "--cases", help="Cases")

args = parser.parse_args()

load_throughputs = []
number_bytes_written_master = []
number_bytes_written_slave1 = []
number_of_compaction = []
number_of_storeFiles = []
number_bytes_read_master=[]
number_bytes_read_slave1=[]
number_bytes_read=[]
load_end_timestamp = []


cases = args.cases.split(':')

for case in cases:
	with open('case'+case+'.log', 'r') as file:
		m = re.findall("\+ echo (\d+)", file.read())
		print(m)
		load_end_timestamp.append(int(m[1]))

# collecting the load throughputs
for case in cases:
	with open(args.caseresult_dir + '/case' + case + '/load_1.dat', 'r') as file:
		for line in file:
			words = line.split()
			if len(words) == 3:
				if words[0] == '[OVERALL],' and words[1] == 'Throughput(ops/sec),':
					load_throughputs.append(float(words[2]))



# collecting metrics
def metricstats(file_name, master, metric):
	metric_val_list=[]
	casecount=-1
	for case in cases:
		if master:
			filename = args.caseresult_dir +  '/case'+ case + '/master/' + file_name
		else:
			filename = args.caseresult_dir + '/case' + case + '/slave1/' + file_name
		casecount=casecount+1
		
		with open(filename, 'r') as file:
			found = False
			f = file.read()
			count = 0
			stamp = load_end_timestamp[casecount]
			while not found and count < 1000:
				regex = "("+str(stamp)+".*)"
				matches = re.findall(regex, f)
				print(matches)
				for match in matches:
					tokens = match.split()
					metric_val=0
					for token in tokens:
						words=token.strip(',').split('=')
						if re.match(metric, words[0]):
							metric_val = metric_val + int(words[1])
							found = True
					if found:
						metric_val_list.append(metric_val)
						break
				stamp = stamp+1
				count=count+1
	return(metric_val_list)


def compactionstats(file_name, master, metric):
	metric_val_list=[]
	casecount=-1
	for case in cases:
		if master:
			filename = args.caseresult_dir +  '/case'+ case + '/master/' + file_name
		else:
			filename = args.caseresult_dir + '/case' + case + '/slave1/' + file_name
		casecount=casecount+1
		
		with open(filename, 'r') as file:
			found = False
			count=0
			stamp = load_end_timestamp[casecount]
			for line in file:
				words=line.split()
				stamplen = len(str(stamp))
				running_stamp = words[0][0:stamplen]
				if stamp > int(running_stamp):
					for word in words:
						kv = word.strip(',').split('=')
						p = re.compile('namespace_default_table_usertable_region_\w*_metric_numFilesCompactedCount')
						if p.match(kv[0]):
							count = count + int(kv[1])
			metric_val_list.append(count)
	return(metric_val_list)


number_bytes_written_master = metricstats( 'datanode-metrics.out', True, 'bytes_written')
number_bytes_written_slave1 = metricstats( 'datanode-metrics.out', False, 'bytes_written')
number_bytes_written = list(map(add, number_bytes_written_master, number_bytes_written_slave1))

number_bytes_read_master = metricstats('datanode-metrics.out', True, 'bytes_read')
number_bytes_read_slave1 = metricstats('datanode-metrics.out', False, 'bytes_read')
number_bytes_read = list(map(add, number_bytes_read_master, number_bytes_read_slave1))

number_storeFiles_master = metricstats('all.metrics', True, 'storeFileCount')
number_storeFiles_slave1 = metricstats('all.metrics', False, 'storeFileCount')
number_storeFiles = list(map(add, number_storeFiles_master, number_storeFiles_slave1))

# collecting the compaction counts

master_number_compaction= compactionstats('all.metrics', True, 'namespace_default_table_usertable_region_\w*_metric_numFilesCompactedCount')
slave_number_compaction= compactionstats('all.metrics', False, 'namespace_default_table_usertable_region_\w*_metric_numberFilesCompactedCount')
number_of_compaction = list(map(add, master_number_compaction, slave_number_compaction))

print(*load_throughputs, sep=',', end='\n')
print(*number_bytes_written, sep=',', end='\n')
#print(*master_number_compaction, sep=',', end='\n')
print(*number_of_compaction, sep=',', end='\n')
print(*number_storeFiles, sep=',', end='\n')
print(*number_bytes_read, sep=',', end='\n')

def make_patch_spines_invisible(ax):
  ax.set_frame_on(True)
  ax.patch.set_visible(False)
    #for sp in ax.spines.itervalues():
    #    sp.set_visible(False)
  for k in ax.spines.keys():
  	ax.spines[k].set_visible(False)

fig, ax1 = pyplot.subplots()
p1, = ax1.plot([1,2,3], load_throughputs, color='r', marker='o', label="insert", linewidth=1.5)
ax2 = ax1.twinx()
p2, = ax2.plot([1,2,3], number_bytes_written, color='b', marker='o', label="byte written", linewidth=1.5)
ax3 = ax1.twinx()
p3, = ax3.plot([1,2,3], number_of_compaction, color='g', marker='o', label="number of compaction", linewidth=1.5)
ax4 = ax1.twinx()
p4, = ax4.plot([1,2,3], number_storeFiles, color='k', marker='o', label="number of storeFiles", linewidth=1.5)
ax5 = ax1.twinx()
p5, = ax5.plot([1,2,3], number_bytes_read, color='c', marker='o', label="byte read", linewidth=1.5)

ax3.spines["right"].set_position(("axes", 1.2))
ax4.spines["right"].set_position(("axes",  1.4)) 
ax5.spines["right"].set_position(("axes", 1.6))

make_patch_spines_invisible(ax3)
make_patch_spines_invisible(ax4)
make_patch_spines_invisible(ax5)

ax3.spines["right"].set_visible(True)
ax4.spines["right"].set_visible(True)
ax5.spines["right"].set_visible(True)

ax1.yaxis.label.set_color(p1.get_color())
ax2.yaxis.label.set_color(p2.get_color())
ax3.yaxis.label.set_color(p3.get_color())
ax4.yaxis.label.set_color(p4.get_color())
ax5.yaxis.label.set_color(p5.get_color())

ax1.set_ylabel('Throughput')
ax2.set_ylabel('byte written')
ax3.set_ylabel('number of compaction')
ax4.set_ylabel('number of storeFiles')
ax5.set_ylabel('byte read')

pyplot.xticks([1,2,3],['Default', 'Major Off', 'Major and Minor Off'], rotation=30)


tkw = dict(size=10, width=1.5)
ax1.tick_params(axis='y', colors=p1.get_color(), **tkw)
ax2.tick_params(axis='y', colors=p2.get_color(), **tkw)
ax3.tick_params(axis='y', colors=p3.get_color(), **tkw)
ax4.tick_params(axis='y', colors=p4.get_color(), **tkw)
ax5.tick_params(axis='y', colors=p5.get_color(), **tkw)
ax1.tick_params(axis='x', **tkw)


lines = [p1, p2, p3, p4, p5]

ax1.legend(lines, [l.get_label() for l in lines])

#pyplot.tight_layout()
#fig.subplots_adjust(right=1)
pyplot.savefig('load_' + args.cases, bbox_inches='tight', pad_inches=0.2)
#pyplot.show()
