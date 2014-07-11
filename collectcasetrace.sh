#!/bin/bash

mkdir caseresult/$1
mkdir caseresult/$1/master
mkdir caseresult/$1/slave1

#copying the rpc trace of hbase
scp hadoop@master:/var/log/hbase/htrace.out caseresult/$1/master/.
scp hadoop@slave1:/var/log/hbase/htrace.out caseresult/$1/slave1/.

#copying hbase metrics
scp hadoop@master:/home/hadoop/hbase/all.metrics caseresult/$1/master/.
scp hadoop@slave1:/home/hadoop/hbase/all.metrics caseresult/$1/slave1/.

#copying dfs metrics
scp hadoop@master:/home/hadoop/hadoop/datanode-metrics.out caseresult/$1/master/.
scp hadoop@slave1:/home/hadoop/hadoop/datanode-metrics.out caseresult/$1/slave1/.
scp hadoop@master:/home/hadoop/hadoop/namenode-metrics.out caseresult/$1/master/.

#hbase logs
scp hadoop@master:/home/hadoop/hbase/logs/hbase-hadoop-master-sceplus-vm48.log caseresult/$1/master/.

scp hadoop@master:/home/hadoop/hbase/logs/hbase-hadoop-regionserver-sceplus-vm48.log caseresult/$1/master/.

scp hadoop@slave1:/home/hadoop/hbase/logs/hbase-hadoop-regionserver-sceplus-vm49.log caseresult/$1/slave1/.

cp $1.log caseresult/$1/.
