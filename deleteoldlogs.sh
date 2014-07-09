#!/bin/bash

rm /var/log/hbase/htrace.out
rm /home/hadoop/hbase/all.metrics
rm /home/hadoop/hadoop/datanode-metrics.out
rm /home/hadoop/hadoop/namenode-metrics.out
rm /home/hadoop/hbase/logs/hbase-hadoop-master-sceplus-vm48.log
rm /home/hadoop/hbase/logs/hbase-hadoop-regionserver-sceplus-vm48.log

ssh hadoop@slave1 rm /var/log/hbase/htrace.out
ssh hadoop@slave1 rm /home/hadoop/hbase/all.metrics
ssh hadoop@slave1 rm /home/hadoop/hadoop/datanode-metrics.out
ssh hadoop@slave1 rm /home/hadoop/hbase/logs/hbase-hadoop-regionserver-sceplus-vm49.log
