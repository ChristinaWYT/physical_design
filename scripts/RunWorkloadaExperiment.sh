#!/bin/bash

set -x

for i in `seq 79 93`;
do
	./deleteoldlogs.sh
	ssh hadoop@master /home/hadoop/hadoop/bin/start-dfs.sh
	ssh hadoop@master /home/hadoop/hbase/bin/start-hbase.sh
	./RunACase.sh clean create workloada &>case`echo $i`.log
	./collectcasetrace.sh case`echo $i`
	ssh hadoop@master /home/hadoop/hbase/bin/stop-hbase.sh
	ssh hadoop@master /home/hadoop/hadoop/bin/stop-dfs.sh
done

set +x
