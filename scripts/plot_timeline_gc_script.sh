#!/bin/bash

python3 plot_timeline_gc.py -caseresult_dir caseresult -cases $1 -metric gc -workload workloadc1 -title "throughput timeline" -ylim 40000 -plot_dir plots/



