#!/bin/bash

mkdir caseresult/$1
mkdir caseresult/$1/master
mkdir caseresult/$1/slave1

#copying the rpc trace of hbase
cp /var/log/hbase/htrace.out caseresult/$1/master/.
scp hadoop@slave1:/var/log/hbase/htrace.out caseresult/$1/slave1/.

#copying hbase metrics
cp /home/hadoop/hbase/all.metrics caseresult/$1/master/.
scp hadoop@slave1:/home/hadoop/hbase/all.metrics caseresult/$1/slave1/.

#copying dfs metrics
cp /home/hadoop/hadoop/datanode-metrics.out caseresult/$1/master/.
scp hadoop@slave1:/home/hadoop/hadoop/datanode-metrics.out caseresult/$1/slave1/.
cp /home/hadoop/hadoop/namenode-metrics.out caseresult/$1/master/.

#hbase logs
cp /home/hadoop/hbase/logs/hbase-hadoop-master-sceplus-vm48.log caseresult/$1/master/.

cp /home/hadoop/hbase/logs/hbase-hadoop-regionserver-sceplus-vm48.log caseresult/$1/master/.

scp hadoop@slave1:/home/hadoop/hbase/logs/hbase-hadoop-regionserver-sceplus-vm49.log caseresult/$1/slave1/.

cp $1.log caseresult/$1/.
