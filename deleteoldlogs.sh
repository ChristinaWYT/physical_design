#!/bin/bash

rm /var/log/hbase/htrace.out
rm /home/hadoop/hbase/all.metrics
rm /home/hadoop/hadoop/datanode-metrics.out
rm /home/hadoop/hadoop/namenode-metrics.out

ssh hadoop@slave1 rm /var/log/hbase/htrace.out
ssh hadoop@slave1 rm /home/hadoop/hbase/all.metrics
ssh hadoop@slave1 rm /home/hadoop/hadoop/datanode-metrics.out
