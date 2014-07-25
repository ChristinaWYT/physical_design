#!/bin/bash

#python3 plot_timeline_allmetrics.py -caseresult_dir caseresult -cases 130:131:132 -metric storeFileCount -workload load -title "Write only workload:storefile timeline" -ylim 1000 -plot_dir plots/ -plot_type='scatter'
#python3 plot_timeline_allmetrics.py -caseresult_dir caseresult -cases 115:116:117 -metric storeFileCount -workload workloadc -title "Write heavy workload:storefile timeline" -ylim 1000 -plot_dir plots/ -plot_type='scatter'


#python3 plot_timeline_allmetrics.py -caseresult_dir caseresult -cases 130:131:132 -metric blockCacheHitCount -workload load -title "Write only workload:block cache hit count timeline" -ylim 1000 -plot_dir plots/ -plot_type='scatter'
#python3 plot_timeline_allmetrics.py -caseresult_dir caseresult -cases 115:116:117 -metric blockCacheHitCount -workload workloadc -title "Write heavy workload:block cache hit count timeline" -ylim 1000 -plot_dir plots/ -plot_type='scatter'


#python3 plot_timeline_allmetrics.py -caseresult_dir caseresult -cases 130:131:132 -metric readBlockOp_avg_time -workload load -title "Write only workload read block avg time timeline" -ylim 1000 -plot_dir plots/ -plot_type scatter -metric_file datanode-metrics.out
#python3 plot_timeline_allmetrics.py -caseresult_dir caseresult -cases 121:122:123 -metric readBlockOp_avg_time -workload load -title "Write only workload read block avg time timeline" -ylim 1000 -plot_dir plots/ -plot_type scatter -metric_file datanode-metrics.out
#python3 plot_timeline_allmetrics.py -caseresult_dir caseresult -cases 79:80:81 -metric readBlockOp_avg_time -workload load -title "Readheavy workload read block avg time timeline" -ylim 1000 -plot_dir plots/ -plot_type scatter -metric_file datanode-metrics.out
#python3 plot_timeline_allmetrics.py -caseresult_dir caseresult -cases 82:83:84 -metric readBlockOp_avg_time -workload load -title "Readheavyworkload read block avg time timeline" -ylim 1000 -plot_dir plots/ -plot_type scatter -metric_file datanode-metrics.out
#python3 plot_timeline_allmetrics.py -caseresult_dir caseresult -cases 109:110:111 -metric readBlockOp_avg_time -workload workloadc -title "Writeheavy workload read block avg time timeline" -ylim 1000 -plot_dir plots/ -plot_type scatter -metric_file datanode-metrics.out
#python3 plot_timeline_allmetrics.py -caseresult_dir caseresult -cases 112:113:114 -metric readBlockOp_avg_time -workload workloadc -title "Writeheavy worklload read block avg time timeline" -ylim 1000 -plot_dir plots/ -plot_type scatter -metric_file datanode-metrics.out
#python3 plot_timeline_allmetrics.py -caseresult_dir caseresult -cases 109:110:111 -metric writeBlockOp_avg_time -workload workloadc -title "Writeheavy workload read block avg time timeline" -ylim 1000 -plot_dir plots/ -plot_type scatter -metric_file datanode-metrics.out
#python3 plot_timeline_allmetrics.py -caseresult_dir caseresult -cases 201:202 -metric throughput -workload workloada -title "Readheavy worklload cachehit timeline" -ylim_max 40000 -ylim_min 50000 -plot_dir plots/ -plot_type scatter -metric_file 
python3 plot_timeline_allmetrics.py -caseresult_dir caseresult -cases 211:212 -metric blockCountHitPercent -workload workloadc -title "Writeheavy worklload cachehit timeline" -ylim_max 100 -ylim_min 90 -plot_dir plots/ -plot_type scatter -metric_file all.metrics 
