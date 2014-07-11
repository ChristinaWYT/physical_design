#!/bin/bash


python3 plot_workloadc.py  -caseresult_dir caseresult -cases 34:35:36 -loc 0 -title Run1
python3 plot_workloadc.py  -caseresult_dir caseresult -cases 37:38:39 -loc 0 -title Run2
python3 plot_workloadc.py  -caseresult_dir caseresult -cases 40:41:42 -loc 0 -title Run3
python3 plot_workloadc.py  -caseresult_dir caseresult -cases 43:44:45 -loc 0 -title Run4
python3 plot_workloadc.py  -caseresult_dir caseresult -cases 46:47:48 -loc 0 -title Run5
	#python3 plot_workloadc_latency.py  -caseresult_dir caseresult -cases run -loc 0
