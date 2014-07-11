#!/bin/bash

python3 plot_load.py  -caseresult_dir caseresult -cases $1
python3 plot_load_latency.py  -caseresult_dir caseresult -cases $1

python3 plot_read.py  -caseresult_dir caseresult -cases $1
python3 plot_read_latency.py  -caseresult_dir caseresult -cases $1

python3 plot_workloada.py  -caseresult_dir caseresult -cases $1
python3 plot_workloada_latency.py  -caseresult_dir caseresult -cases $1

python3 plot_workloadb.py  -caseresult_dir caseresult -cases $1
python3 plot_workloadb_latency.py  -caseresult_dir caseresult -cases $1

python3 plot_workloadc.py  -caseresult_dir caseresult -cases $1
python3 plot_workloadc_latency.py  -caseresult_dir caseresult -cases $1
