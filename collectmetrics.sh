#!/bin/bash

mkdir results/$1
mkdir results/$1/master
mkdir results/$1/slave1

#copying the rpc trace of hbase
cp /var/log/hbase/htrace.out results/$1/master/.
scp hadoop@slave1:/var/log/hbase/htrace.out results/$1/slave1/.

#copying hbase metrics
cp /home/hadoop/hbase/all.metrics results/$1/master/.
scp hadoop@slave1:/home/hadoop/hbase/all.metrics results/$1/slave1/.

#copying dfs metrics
cp /home/hadoop/hadoop/datanode-metrics.out results/$1/master/.
scp hadoop@slave1:/home/hadoop/hadoop/datanode-metrics.out results/$1/master/.
cp /home/hadoop/hadoop/namenode-metrics.out results/$1/master/.

#hbase logs
cp /home/hadoop/hbase/logs/hbase-hadoop-master-sceplus-vm48.log results/$1/master/.

cp /home/hadoop/hbase/logs/hbase-hadoop-regionserver-sceplus-vm48.log results/$1/slave1/.

scp hadoop@slave1:/home/hadoop/hbase/logs/hbase-hadoop-regionserver-sceplus-vm49.log results/$1/slave1/.

#copying experiment log
cp /home/hadoop/ycsb-0.1.4/create_*.script results/$1/.
cp /home/hadoop/ycsb-0.1.4/*.dat results/$1/. 
cp experiment.sh results/$1/.
cp experiments.list* results/$1/.
cp $1.log results/$1/.
cp /home/hadoop/ycsb-0.1.4/scan results/$1/.
cp /home/hadoop/ycsb-0.1.4/random_read results/$1/.
cp /home/hadoop/ycsb-0.1.4/ld results/$1/.
cp /home/hadoop/ycsb-0.1.4/workloads/* results/$1/.
