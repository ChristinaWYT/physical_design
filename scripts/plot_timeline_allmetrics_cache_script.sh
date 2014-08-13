#!/bin/bash

#python3 plot_timeline_allmetrics_cache.py -caseresult_dir caseresult -cases 298 -metric dummy -workload workloadb -title "worklload cachehit timeline" -ylim_max 11 -ylim_min 1 -plot_dir plots/ -plot_type scatter -metric_file all.metrics 
#python3 plot_timeline_allmetrics_cache.py -caseresult_dir caseresult -cases 299 -metric dummy -workload workloadc -title "worklload cachehit timeline" -ylim_max 11 -ylim_min 1 -plot_dir plots/ -plot_type scatter -metric_file all.metrics 
#python3 plot_timeline_allmetrics_cache.py -caseresult_dir caseresult -cases 300 -metric dummy -workload workloada -title "worklload cachehit timeline" -ylim_max 11 -ylim_min 1 -plot_dir plots/ -plot_type scatter -metric_file all.metrics 
#python3 plot_timeline_allmetrics_cache.py -caseresult_dir caseresult -cases 301 -metric dummy -workload workloadb -title "worklload cachehit timeline" -ylim_max 11 -ylim_min 1 -plot_dir plots/ -plot_type scatter -metric_file all.metrics 
#python3 plot_timeline_allmetrics_cache.py -caseresult_dir caseresult -cases 302 -metric dummy -workload workloadc -title "worklload cachehit timeline" -ylim_max 11 -ylim_min 1 -plot_dir plots/ -plot_type scatter -metric_file all.metrics 
#python3 plot_timeline_allmetrics_cache.py -caseresult_dir caseresult -cases 303 -metric dummy -workload workloada -title "worklload cachehit timeline" -ylim_max 11 -ylim_min 1 -plot_dir plots/ -plot_type scatter -metric_file all.metrics 
#python3 plot_timeline_allmetrics_cache.py -caseresult_dir caseresult -cases 305 -metric dummy -workload workloadc -title "worklload cachehit timeline" -ylim_max 11 -ylim_min 1 -plot_dir plots/ -plot_type scatter -metric_file all.metrics 
#python3 plot_timeline_allmetrics_cache.py -caseresult_dir caseresult -cases 307 -metric dummy -workload workloadc -title "worklload cachehit timeline" -ylim_max 11 -ylim_min 0 -plot_dir plots/ -plot_type scatter -metric_file all.metrics 
python3 plot_timeline_allmetrics_cache.py -caseresult_dir caseresult -cases $1 -metric dummy -workload workloadc -title "worklload cachehit timeline" -ylim_max 11 -ylim_min 0 -plot_dir plots/ -plot_type scatter -metric_file all.metrics 
