#! /bin/bash 

for i in `seq 231 236`
do
	python3 AppendCaseSummary.py -caseresult_dir caseresult -case $i -loc 0 -cluster_config_type 2 -hbase_config_type 2 -table_config_type 1 -phase 1
done
