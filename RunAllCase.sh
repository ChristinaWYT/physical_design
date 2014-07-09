#!/bin/bash

set -x

for i in `seq 30 33`;
do
	./deleteoldlogs.sh
	start-dfs.sh
	start-hbase.sh
	./RunACase.sh all &>case`echo $i`.log
	./collectcasetrace.sh case`echo $i`
	stop-hbase.sh
	stop-dfs.sh
done

set +x
