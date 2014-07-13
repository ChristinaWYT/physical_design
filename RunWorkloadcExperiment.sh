#!/bin/bash

set -x

for i in `seq 94 108`;
do
	./deleteoldlogs.sh
	start-dfs.sh
	start-hbase.sh
	./RunACase.sh clean create workloadc &>case`echo $i`.log
	./collectcasetrace.sh case`echo $i`
	stop-hbase.sh
	stop-dfs.sh
done

set +x
