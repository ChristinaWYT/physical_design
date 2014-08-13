#!/bin/bash

python3 plot_timeline_cache.py -caseresult_dir caseresult -cases 298 -metric max  -workload workloadb -title "Read-Write worklload cachehit timeline" -ylim_max 11 -ylim_min 0 -plot_dir plots/ -metric_file hbase-hadoop-regionserver-sceplus-vm49.log 
