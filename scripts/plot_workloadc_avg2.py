import re
import matplotlib.pyplot as pyplot
import numpy as np
import argparse
from operator import add
from operator import sub

data_dict=dict()
counter=1
localcounter=1
with open('plot_workloadc495051.dat','r') as file:
	for line in file:
		data_dict[counter, localcounter]=line.strip().split(',')
		print(data_dict[(counter, localcounter)])
		localcounter=localcounter+1

localcounter=1
counter=counter+1

with open('plot_workloadc525354.dat','r') as file:
	for line in file:
		data_dict[counter, localcounter]=line.strip().split(',')
		print(data_dict[(counter, localcounter)])
		localcounter=localcounter+1

localcounter=1
counter=counter+1
with open('plot_workloadc555657.dat','r') as file:
	for line in file:
		data_dict[counter, localcounter]=line.strip().split(',')
		print(data_dict[(counter, localcounter)])
		localcounter=localcounter+1

localcounter=1
counter=counter+1
with open('plot_workloadc585960.dat','r') as file:
	for line in file:
		data_dict[counter, localcounter]=line.strip().split(',')
		print(data_dict[(counter, localcounter)])
		localcounter=localcounter+1

counter=counter+1
localcounter=1
with open('plot_workloadc616263.dat','r') as file:
	for line in file:
		data_dict[counter, localcounter]=line.strip().split(',')
		print(data_dict[(counter, localcounter)])
		localcounter=localcounter+1


avg=dict()

for r in [1,2,3,5]:
	s=[0,0,0]
	for f in [1,2,3,4,5]:
		s = list(map(add, s, [float(x) for x in data_dict[f, r]]))
		#print([float(x) for x in data_dict[f,r]])
	#print(s)
	avg[r]= [x/5 for x in s]



def make_patch_spines_invisible(ax):
  ax.set_frame_on(True)
  ax.patch.set_visible(False)
    #for sp in ax.spines.itervalues():
    #    sp.set_visible(False)
  for k in ax.spines.keys():
        ax.spines[k].set_visible(False)


#print(*avg_throughputs, sep=',', end='\n')
print(*avg[1], sep=',', end='\n')
#print(*avg_bytes_written, sep=',', end='\n')
print(*avg[2], sep=',', end='\n')
#print(*avg_compaction, sep=',', end='\n')
print(*avg[3], sep=',', end='\n')
#print(*avg_bytes_read, sep=',', end='\n')	
print(*avg[5], sep=',', end='\n')	

workloadc_throughputs=avg[1]
number_bytes_written=avg[2]
#print(*master_number_compaction, sep=',', end='\n')
number_of_compaction=avg[3]
#number_storeFiles=avg[4]
number_bytes_read=avg[5]

fig, ax1 = pyplot.subplots()
fig.subplots_adjust(right=0.75)
p1, = ax1.plot([1,2,3], workloadc_throughputs, color='r', marker='o', label="workloadc throughput", linewidth=1.5)
ax2 = ax1.twinx()
p2, = ax2.plot([1,2,3], number_bytes_written, color='b', marker='o', label="byte written", linewidth=1.5)
ax3 = ax1.twinx()
p3, = ax3.plot([1,2,3], number_of_compaction, color='g', marker='o', label="number of compaction", linewidth=1.5)

#ax4 = ax1.twinx()
#p4, = ax4.plot([1,2,3], number_storeFiles, color='k', marker='o', label="change in number of storeFiles")
ax5 = ax1.twinx()
p5, = ax5.plot([1,2,3], number_bytes_read, color='c', marker='o', label="byte read", linewidth=1.5)

ax3.spines["right"].set_position(("axes", 1.1))
#ax4.spines["right"].set_position(("axes",  1.2))
ax5.spines["right"].set_position(("axes", 1.3))

make_patch_spines_invisible(ax3)
#make_patch_spines_invisible(ax4)
make_patch_spines_invisible(ax5)

ax3.spines["right"].set_visible(True)
#ax4.spines["right"].set_visible(True)
ax5.spines["right"].set_visible(True)

make_patch_spines_invisible(ax3)
#make_patch_spines_invisible(ax4)
make_patch_spines_invisible(ax5)

ax3.spines["right"].set_visible(True)
#ax4.spines["right"].set_visible(True)
ax5.spines["right"].set_visible(True)

ax1.yaxis.label.set_color(p1.get_color())
ax2.yaxis.label.set_color(p2.get_color())
ax3.yaxis.label.set_color(p3.get_color())
#ax4.yaxis.label.set_color(p4.get_color())
ax5.yaxis.label.set_color(p5.get_color())

ax1.set_ylabel('Throughput')
ax2.set_ylabel('byte written')
ax3.set_ylabel('number of compaction')
#ax4.set_ylabel('change in number of storeFiles')
ax5.set_ylabel('byte read')

pyplot.xticks([1,2,3],['Default', 'Major Off', 'Major and Minor Off'], rotation=30)


tkw = dict(size=10, width=1.5)
ax1.tick_params(axis='y', colors=p1.get_color(), **tkw)
ax2.tick_params(axis='y', colors=p2.get_color(), **tkw)
ax3.tick_params(axis='y', colors=p3.get_color(), **tkw)
#ax4.tick_params(axis='y', colors=p4.get_color(), **tkw)
ax5.tick_params(axis='y', colors=p5.get_color(), **tkw)
ax1.tick_params(axis='x', **tkw)

#lines = [p1, p2, p3, p4, p5]
lines = [p1, p2, p3,  p5]

ax1.legend(lines, [l.get_label() for l in lines])

pyplot.title('Avg 2')
pyplot.savefig('plot_workloadc_avg_2', bbox_inches='tight', pad_inches=0.2)

