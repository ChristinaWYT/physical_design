#!/bin/bash

set -x

for i in `seq $2 $3`;
do
	./deleteoldlogs.sh
	scp hadoop@master:/home/hadoop/hbase/conf/hbase-site.xml.`echo $4` hadoop@master:/home/hadoop/hbase/conf/hbase-site.xml
	scp hadoop@master:/home/hadoop/hbase/conf/hbase-site.xml.`echo $4` hadoop@slave1:/home/hadoop/hbase/conf/hbase-site.xml
	ssh hadoop@master /home/hadoop/hadoop/sbin/start-dfs.sh
	ssh hadoop@master /home/hadoop/hbase/bin/start-hbase.sh
	scp /home/hadoop/git/physical_design/read_`echo $6` hadoop@master:/home/hadoop/hbase/readpropfile 
	scp /home/hadoop/git/physical_design/read_`echo $6` hadoop@slave1:/home/hadoop/hbase/readpropfile
	scp /home/hadoop/git/physical_design/mem_threshold_`echo $6` hadoop@master:/home/hadoop/hbase/mem_thresholdfile
	scp /home/hadoop/git/physical_design/mem_threshold_`echo $6` hadoop@slave1:/home/hadoop/hbase/mem_thresholdfile
	scp /home/hadoop/git/physical_design/evict_threshold_`echo $7` hadoop@master:/home/hadoop/hbase/evict_thresholdfile
	scp /home/hadoop/git/physical_design/evict_threshold_`echo $7` hadoop@slave1:/home/hadoop/hbase/evict_thresholdfile
	scp /home/hadoop/git/physical_design/cachevalue_`echo $6` hadoop@master:/home/hadoop/hbase/cachevaluefile
	scp /home/hadoop/git/physical_design/cachevalue_`echo $6` hadoop@slave1:/home/hadoop/hbase/cachevaluefile
	filename="case"`ls caseresult/ -ltr | wc -l` 
	mkdir caseresult/$filename
	ssh hadoop@master mkdir /home/hadoop/git/physical_design/caseresult/$filename
	./RunACase.sh $filename clean create $1 $5  &>case`echo $i`.log
	#scp /home/hadoop/git/physical_design/read_1 hadoop@master:/home/hadoop/hbase/readpropfile 
	#scp /home/hadoop/git/physical_design/read_1 hadoop@slave1:/home/hadoop/hbase/readpropfile 
	#./RunACase.sh $filename workloadc1 $5 &>case`echo $i`_1.log
	./collectcasetrace.sh case`echo $i`
	ssh hadoop@master /home/hadoop/hbase/bin/stop-hbase.sh
	ssh hadoop@master /home/hadoop/hadoop/sbin/stop-dfs.sh
done

set +x
