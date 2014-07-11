#!/bin/bash 

python3 plot_timeline.py -caseresult_dir caseresult -cases 34:35:36 -metric throughput
python3 plot_timeline.py -caseresult_dir caseresult -cases 37:38:39 -metric throughput
python3 plot_timeline.py -caseresult_dir caseresult -cases 40:41:42 -metric throughput
python3 plot_timeline.py -caseresult_dir caseresult -cases 43:44:45 -metric throughput
python3 plot_timeline.py -caseresult_dir caseresult -cases 46:47:48 -metric throughput


python3 plot_timeline.py -caseresult_dir caseresult -cases 34:35:36 -metric read_latency
python3 plot_timeline.py -caseresult_dir caseresult -cases 37:38:39 -metric read_latency
python3 plot_timeline.py -caseresult_dir caseresult -cases 40:41:42 -metric read_latency
python3 plot_timeline.py -caseresult_dir caseresult -cases 43:44:45 -metric read_latency
python3 plot_timeline.py -caseresult_dir caseresult -cases 46:47:48 -metric read_latency


python3 plot_timeline.py -caseresult_dir caseresult -cases 34:35:36 -metric write_latency
python3 plot_timeline.py -caseresult_dir caseresult -cases 37:38:39 -metric write_latency
python3 plot_timeline.py -caseresult_dir caseresult -cases 40:41:42 -metric write_latency
python3 plot_timeline.py -caseresult_dir caseresult -cases 43:44:45 -metric write_latency
python3 plot_timeline.py -caseresult_dir caseresult -cases 46:47:48 -metric write_latency
