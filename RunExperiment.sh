#!/bin/bash

set -x

for i in `seq $2 $3`;
do
	./deleteoldlogs.sh
	scp hadoop@master:/home/hadoop/hbase/conf/hbase-site.xml.`echo $4` hadoop@master:/home/hadoop/hbase/conf/hbase-site.xml
	scp hadoop@master:/home/hadoop/hbase/conf/hbase-site.xml.`echo $4` hadoop@slave1:/home/hadoop/hbase/conf/hbase-site.xml
	ssh hadoop@master /home/hadoop/hadoop/bin/start-dfs.sh
	ssh hadoop@master /home/hadoop/hbase/bin/start-hbase.sh
	./RunACase.sh clean create $1 $5 &>case`echo $i`.log
	./collectcasetrace.sh case`echo $i`
	ssh hadoop@master /home/hadoop/hbase/bin/stop-hbase.sh
	ssh hadoop@master /home/hadoop/hadoop/bin/stop-dfs.sh
done

set +x
