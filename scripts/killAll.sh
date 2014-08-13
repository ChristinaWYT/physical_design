#!/bin/bash

ssh master jps | grep HMaster | kill -9 `awk '{print $1}'`
ssh master jps | grep HQuorumPeer | kill -9 `awk '{print $1}'`
ssh master jps | grep HRegionServer | kill -9 `awk '{print $1}'`
ssh master rm /var/hadoop/pids/*

ssh slave1 jps | grep HQuorumPeer | kill -9 `awk '{print $1}'`
ssh slave1 jps | grep HRegionServer | kill -9 `awk '{print $1}'`
ssh slave1 rm /var/hadoop/pids/*
