import re

import argparse
from operator import add
from operator import sub


parser = argparse.ArgumentParser()

parser.add_argument("-caseresult_dir", "--caseresult_dir", help="Result Dir")
parser.add_argument("-case", "--case", help="Case")
parser.add_argument("-loc", "--loc", help="loc")
parser.add_argument("-cluster_config_type", "--cluster_config_type",help="cluster config type")
parser.add_argument("-hbase_config_type", "--hbase_config_type",help="hbase config type")
parser.add_argument("-table_config_type", "--table_config_type",help="table config type")
parser.add_argument("-phase","--phase",help="Phase")
#parser.add_argument("-workload_type","--workload_type",help="workload type")
args = parser.parse_args()

#extract the workload type
def get_workload_type():
	workload_type=''
	with open(args.caseresult_dir + '/case' + args.case + '/case' + args.case + '.log', 'r') as caselog:
		f = caselog.read()
		if re.findall('\+ load=true', f):
			workload_type='load'
		elif re.findall('\+ random_read=true', f):
			workload_type='random_read'
		elif re.findall('\+ workloada=true', f):
			workload_type='workloada'
		elif re.findall('\+ workloadb=true', f):
			workload_type='workloadb'
		elif re.findall('\+ workloadc=true', f):
			workload_type='workloadc'
		return workload_type

workload_type = get_workload_type()
print(workload_type)
summary = args.case+ ',' + args.cluster_config_type + ',' + args.hbase_config_type + ',' + args.table_config_type + ',' + args.phase + ',' + workload_type + ','

def getNumOperations(filename, operation_type):
	number_of_operations=0
	with open(filename, 'r')  as ycsb_log:
		for line in ycsb_log:
			words = line.strip().split()
			if len(words) == 3:	
				if words[0] == '[' + operation_type  + '],'  and words[1] == 'Operations,':
					number_of_operations = int(words[2])
	return number_of_operations

def getThroughput(filename):
	throuput=0.0
	with open(filename, 'r') as ycsb_log:
		for line in ycsb_log:
			words = line.strip().split()
			if len(words) == 3:
				if words[0] == '[OVERALL],' and words[1] == 'Throughput(ops/sec),':
					throughput = float(words[2])
	return throughput

def getAvgLatency(filename, operation_type):
	avg_latency = 0
	with open(filename, 'r') as ycsb_log:
		for line in ycsb_log:
			words = line.strip().split()
			if len(words) == 3:
				if words[0] == '['+ operation_type  + '],' and words[1] == 'AverageLatency(us),':
					avg_latency = float(words[2])
	return avg_latency



number_of_insert_ops = getNumOperations( args.caseresult_dir + '/case' + args.case + '/' + workload_type + '_1.dat', 'INSERT')
number_of_update_ops = getNumOperations( args.caseresult_dir + '/case' + args.case + '/' + workload_type + '_1.dat', 'UPDATE')
number_of_read_ops = getNumOperations( args.caseresult_dir + '/case' + args.case + '/' + workload_type + '_1.dat', 'READ')
number_of_scan_ops = getNumOperations( args.caseresult_dir + '/case' + args.case + '/' + workload_type + '_1.dat', 'SCAN')
number_of_delete_ops = getNumOperations( args.caseresult_dir + '/case' + args.case + '/' + workload_type + '_1.dat', 'DELETE')
total_number_ops = number_of_insert_ops + number_of_update_ops + number_of_read_ops + number_of_scan_ops + number_of_delete_ops


summary = summary + str(total_number_ops) + ','
summary = summary + str(getThroughput( args.caseresult_dir + '/case' + args.case + '/' + workload_type + '_1.dat')) + ','

def getAsyncProcessErrorCount(filename):
	errorCount=0
	with open(filename, 'r') as caselog:
		for line in caselog:
			tokens = line.strip().split()
	return errorCount

summary = summary + str(number_of_insert_ops) + ','
summary = summary + str(getAvgLatency( args.caseresult_dir + '/case' + args.case + '/' + workload_type + '_1.dat', 'INSERT')) + ','
summary = summary + str(number_of_read_ops) + ','
summary = summary + str(getAvgLatency( args.caseresult_dir + '/case' + args.case + '/' + workload_type + '_1.dat', 'READ')) + ','
summary = summary + str(number_of_update_ops) + ','
summary = summary + str(getAvgLatency( args.caseresult_dir + '/case' + args.case + '/' + workload_type + '_1.dat', 'UPDATE')) + ','
summary = summary + str(number_of_scan_ops) + ','
summary = summary + str(getAvgLatency( args.caseresult_dir + '/case' + args.case + '/' + workload_type + '_1.dat', 'SCAN')) + ','
summary = summary + str(number_of_delete_ops) + ','
summary = summary + str(getAvgLatency( args.caseresult_dir + '/case' + args.case + '/' + workload_type + '_1.dat', 'DELETE')) + ','

def getMetric(filename, metric):
	metric_val=0
	with open(filename, 'r') as file:
		for line in file:
			tokens = line.strip().split()
			for token in tokens:
				words=token.strip(',').split('=')
				if metric == words[0]:
					metric_val = float(words[1])
	return(metric_val)

def get_avgtime_metric(filename1, filename2, metric1, metric2):
	metric_val=0
	master_total_ops=0
	master_total_opstime=0
	with open(args.caseresult_dir + '/case' + args.case + filename1, 'r') as master_datanode_metric:
		for line in master_datanode_metric:
			tokens = line.strip().split()
			for token in tokens:
				words=token.strip(',').split('=')
				if metric1 == words[0]:
					ops = float(words[1])
				if metric2 == words[0]:
					ops_avg_time = float(words[1])
					master_total_opstime = master_total_opstime + ops_avg_time*(ops - master_total_ops)
					#print('master total ops time: ' + str(master_total_opstime))
					#print('master total num ops: ' + str(ops))
					master_total_ops=ops

	slave1_total_ops=0
	slave1_total_opstime=0
	with open(args.caseresult_dir + '/case' + args.case + filename2, 'r') as slave1_datanode_metric:
		for line in slave1_datanode_metric:
			tokens = line.strip().split()
			for token in tokens:
				words=token.strip(',').split('=')
				if metric1 == words[0]:
					ops = float(words[1])
				if metric2 == words[0]:
					ops_avg_time = float(words[1])
					slave1_total_opstime = slave1_total_opstime + ops_avg_time*(ops - slave1_total_ops)
					#print('slave1 total ops time: ' + str(slave1_total_opstime))
					#print('slave1 total num ops: ' + str(ops))
					slave1_total_ops=ops

	metric_val = (master_total_opstime+slave1_total_opstime)/(master_total_ops+slave1_total_ops)
	return metric_val

summary = summary + str(getMetric(args.caseresult_dir + '/case' + args.case + '/master/namenode-metrics.out', 'CapacityUsed')/(1024*1024*1024)) + ','

def get_dfs_metric(metric):
	dfs_master_metric_val = getMetric(args.caseresult_dir + '/case' + args.case + '/master/datanode-metrics.out', metric)
	dfs_slave1_metric_val = getMetric(args.caseresult_dir + '/case' + args.case + '/slave1/datanode-metrics.out', metric) 
	dfs_metric_val = float(dfs_master_metric_val) + float(dfs_slave1_metric_val)
	return dfs_metric_val

summary = summary + str(get_dfs_metric('bytes_written')/(1024*1024*1024)) + ','
summary = summary + str(get_dfs_metric('bytes_read')/(1024*1024*1024)) + ','
summary = summary + str(get_dfs_metric('blocks_written')) + ','
summary = summary + str(get_dfs_metric('blocks_read')) + ','
summary = summary + str(get_dfs_metric('writes_from_remote_client')) + ','
summary = summary + str(get_dfs_metric('writes_from_local_client')) + ','
summary = summary + str(get_dfs_metric('reads_from_remote_client')) + ','
summary = summary + str(get_dfs_metric('reads_from_local_client')) + ','
summary = summary + str(get_dfs_metric('readBlockOp_num_ops')) + ','
summary = summary + str(get_avgtime_metric('/master/datanode-metrics.out', '/slave1/datanode-metrics.out', 'readBlockOp_num_ops', 'readBlockOp_avg_time')) + ','
summary = summary + str(get_dfs_metric('writeBlockOp_num_ops')) + ','
summary = summary + str(get_avgtime_metric('/master/datanode-metrics.out', '/slave1/datanode-metrics.out', 'writeBlockOp_num_ops', 'writeBlockOp_avg_time')) + ','
summary = summary + str(get_dfs_metric('gcTimeMillis')) + ','

def get_from_all_metric(metric):
	master_metric_val = getMetric(args.caseresult_dir + '/case' + args.case + '/master/all.metrics', metric)
	slave1_metric_val = getMetric(args.caseresult_dir + '/case' + args.case + '/slave1/all.metrics', metric) 
	metric_val = float(master_metric_val) + float(slave1_metric_val)
	return metric_val

summary = summary + str(get_from_all_metric('storeFileCount')) + ','
summary = summary + str(get_from_all_metric('storeFileSize')/(1024*1024*1024)) + ','
summary = summary + str(get_from_all_metric('hlogFileCount')) + ','
summary = summary + str(get_from_all_metric('hlogFileSize')/(1024*1024*1024)) + ','
summary = summary + str(get_from_all_metric('blockCacheFreeSize')/(1024*1024*1024)) + ','
summary = summary + str(get_from_all_metric('blockCacheCount')) + ','
summary = summary + str(get_from_all_metric('blockCacheSize')/(1024*1024*1024)) + ','
summary = summary + str(get_from_all_metric('blockCacheHitCount')) + ','
summary = summary + str(get_from_all_metric('blockCacheMissCount')) + ','
summary = summary + str(get_from_all_metric('blockCacheEvictionCount')) + ','
summary = summary + str(get_from_all_metric('gcTimeMillis')) + ','

def getSummationOfMetric(filename, metric, avg):
	metric_val=0
	count=0
	with open(filename, 'r') as file:
		for line in file:
			words=line.split()
			for word in words:
				kv = word.strip(',').split('=')
				p = re.compile(metric)
				if p.match(kv[0]):
					metric_val = metric_val + int(kv[1])
					count=count+1
	if avg == True:
		metric_val=metric_val/count
	return metric_val

def getTotalCompactionMetric(metric):
	master_compactionMetric = getSummationOfMetric(args.caseresult_dir + '/case' + args.case + '/master/all.metrics', metric, False)
	slave1_compactionMetric = getSummationOfMetric(args.caseresult_dir + '/case' + args.case + '/slave1/all.metrics', metric, False) 
	compactionMetric = int(master_compactionMetric) + int(slave1_compactionMetric)
	return compactionMetric
	
summary = summary + str(getTotalCompactionMetric('namespace_default_table_usertable_region_\w*_metric_numBytesCompactedCount')/(1024*1024*1024)) + ','
summary = summary + str(getTotalCompactionMetric('namespace_default_table_usertable_region_\w*_metric_numFilesCompactedCount')) + ','
summary = summary + str(getTotalCompactionMetric('namespace_default_table_usertable_region_\w*_metric_compactionsCompletedCount')) + ','

def getAvgQueueSize(metric):
	master_queueSize = getSummationOfMetric(args.caseresult_dir + '/case' + args.case + '/master/all.metrics', metric, True)
	slave1_queueSize = getSummationOfMetric(args.caseresult_dir + '/case' + args.case + '/slave1/all.metrics', metric, True)
	avg_queueSize = .5*(master_queueSize+slave1_queueSize)
	return avg_queueSize

summary = summary + str(getAvgQueueSize('queueSize')/1000000) + ','

summary = summary + str(get_avgtime_metric('/master/all.metrics', '/slave1/all.metrics', 'get_num_ops', 'get_mean')) 

with open('collected_metrics.csv','a') as out:
	out.write(summary+'\n')

