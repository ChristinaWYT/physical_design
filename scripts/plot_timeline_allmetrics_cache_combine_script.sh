#!/bin/bash

#python3 plot_timeline_allmetrics_cache_combine.py -caseresult_dir caseresult -cases 301:302:303 -metric dummy -workload workloadb -title "worklload cachehit timeline" -ylim_max 11 -ylim_min 1 -plot_dir plots/ -plot_type scatter -metric_file all.metrics 
#python3 plot_timeline_allmetrics_cache_combine.py -caseresult_dir caseresult -cases 308:309 -metric dummy -workload workloadb -title "worklload cachehit timeline" -ylim_max 11 -ylim_min 1 -plot_dir plots/ -plot_type scatter -metric_file all.metrics 
#python3 plot_timeline_allmetrics_cache_combine.py -caseresult_dir caseresult -cases 310:311:312 -metric dummy -workload workloadc -title "worklload cachehit timeline" -ylim_max 11 -ylim_min 1 -plot_dir plots/ -plot_type scatter -metric_file all.metrics 
python3 plot_timeline_allmetrics_cache_combine.py -caseresult_dir caseresult -cases $1 -metric dummy -workload workloadc -title "workload cachehit timeline" -ylim_max 11 -ylim_min 1 -plot_dir plots/ -plot_type scatter -metric_file all.metrics 
