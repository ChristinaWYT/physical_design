#!/bin/bash

ssh hadoop@master rm /var/log/hbase/htrace.out
ssh hadoop@master rm /home/hadoop/hbase/all.metrics
ssh hadoop@master rm /home/hadoop/hadoop/datanode-metrics.out
ssh hadoop@master rm /home/hadoop/hadoop/namenode-metrics.out
ssh hadoop@master rm /home/hadoop/hbase/logs/hbase-hadoop-master-sceplus-vm48.log
ssh hadoop@master rm /home/hadoop/hbase/logs/hbase-hadoop-master-sceplus-vm48.log.1
ssh hadoop@master rm /home/hadoop/hbase/logs/hbase-hadoop-master-sceplus-vm48.out
ssh hadoop@master rm /home/hadoop/hbase/logs/hbase-hadoop-master-sceplus-vm48.out.1

ssh hadoop@master rm /home/hadoop/hbase/logs/hbase-hadoop-regionserver-sceplus-vm48.log

ssh hadoop@slave1 rm /var/log/hbase/htrace.out
ssh hadoop@slave1 rm /home/hadoop/hbase/all.metrics
ssh hadoop@slave1 rm /home/hadoop/hadoop/datanode-metrics.out
ssh hadoop@slave1 rm /home/hadoop/hbase/logs/hbase-hadoop-regionserver-sceplus-vm49.log
ssh hadoop@slave1 rm /home/hadoop/hbase/logs/hbase-hadoop-regionserver-sceplus-vm49.out

ssh hadoop@slave1 rm /home/hadoop/hbase/logs/hbase-hadoop-regionserver-sceplus-vm49.log.1
ssh hadoop@slave1 rm /home/hadoop/hbase/logs/hbase-hadoop-regionserver-sceplus-vm49.out.1
