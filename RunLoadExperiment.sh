#!/bin/bash

set -x

for i in `seq 64 78`;
do
	./deleteoldlogs.sh
	start-dfs.sh
	start-hbase.sh
	./RunACase.sh clean create load &>case`echo $i`.log
	./collectcasetrace.sh case`echo $i`
	stop-hbase.sh
	stop-dfs.sh
done

set +x
