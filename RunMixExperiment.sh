#!/bin/bash

set -x

for i in `seq $2 $3`;
do
	./deleteoldlogs.sh
	scp hadoop@master:/home/hadoop/hbase/conf/hbase-site.xml.`echo $4` hadoop@master:/home/hadoop/hbase/conf/hbase-site.xml
	scp hadoop@master:/home/hadoop/hbase/conf/hbase-site.xml.`echo $4` hadoop@slave1:/home/hadoop/hbase/conf/hbase-site.xml
	ssh hadoop@master /home/hadoop/hadoop/sbin/start-dfs.sh
	ssh hadoop@master /home/hadoop/hbase/bin/start-hbase.sh
	
	filename="case"`ls caseresult/ -ltr | wc -l` 
	mkdir caseresult/$filename
	ssh hadoop@master mkdir /home/hadoop/git/physical_design/caseresult/$filename
	
	scp /home/hadoop/git/physical_design/read_10 hadoop@master:/home/hadoop/hbase/readpropfile 
	scp /home/hadoop/git/physical_design/read_10 hadoop@slave1:/home/hadoop/hbase/readpropfile
	./RunACase.sh $filename clean create workloadc $5  &>case`echo $i`_1.log
       
 	
	scp /home/hadoop/git/physical_design/read_90 hadoop@master:/home/hadoop/hbase/readpropfile 
	scp /home/hadoop/git/physical_design/read_90 hadoop@slave1:/home/hadoop/hbase/readpropfile
	./RunACase.sh $filename workloada $5  &>case`echo $i`_2.log

        		
	scp /home/hadoop/git/physical_design/read_50 hadoop@master:/home/hadoop/hbase/readpropfile 
	scp /home/hadoop/git/physical_design/read_50 hadoop@slave1:/home/hadoop/hbase/readpropfile
	./RunACase.sh $filename workloadb $5  &>case`echo $i`_3.log

	
	scp /home/hadoop/git/physical_design/read_1 hadoop@master:/home/hadoop/hbase/readpropfile 
	scp /home/hadoop/git/physical_design/read_1 hadoop@slave1:/home/hadoop/hbase/readpropfile
	./RunACase.sh $filename workloadc1 $5  &>case`echo $i`_4.log
	

	./collectcasetrace.sh case`echo $i`
	ssh hadoop@master /home/hadoop/hbase/bin/stop-hbase.sh
	ssh hadoop@master /home/hadoop/hadoop/sbin/stop-dfs.sh
done

set +x
