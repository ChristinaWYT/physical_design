#!/bin/bash

set -x
filename=$1
requestdistribution=''
RESULT_DIR=/home/hadoop/git/physical_design/caseresult/$filename
TEN=10
SIXTY=60
SLEEP_TIME=60
YCSB_DIR=/home/hadoop/ycsb-0.1.4
number_of_operations=25000000
number_of_threads=20
number_of_records=25000000
output_file_suffix='.dat'
experiment_list_file=/home/hadoop/git/physical_design/case_dir/$filename".list"
clean=false
create=false
load=false
random_read=false
workloada=false
workloadb=false
workloadc=false
workloadc1=false
scan=false
all=false

for i in $@
do
        if [ "$i" == "all" ]
	then
		all=true
	elif [ "$i" == "clean" ]
	then
		clean=true
	elif [ "$i" == "create" ]
	then
		create=true
	elif [ "$i" == "load" ]
	then
		load=true
	elif [ "$i" == "random_read" ]
	then
		random_read=true
	elif [ "$i" == "scan" ]
	then
		scan=true
	elif [ "$i" == "workloada" ]
	then
		workloada=true
	elif [ "$i" == "workloadb" ]
	then
		workloadb=true
	elif [ "$i" == "workloadc" ]
	then
		workloadc=true
	elif [ "$i" == "workloadc1" ]
	then
		workloadc1=true
	elif [ "$i" == "zipfian" ]
	then
		requestdistribution="zipfian"
	elif [ "$i" == "uniform" ]
	then
		requestdistribution="uniform"
	fi
done

let counter=1

function create_table {
	echo "creating table..."
	echo $1
	ssh hadoop@master /home/hadoop/hbase/bin/hbase shell $1
}


cd $YCSB_DIR
echo `pwd`

while read line
do
	if $all || $clean
	then
		echo "sleeping for $SIXTY ..."
		sleep $SIXTY
		echo "droping usertable..."
		ssh hadoop@slave1 /home/hadoop/hbase/bin/hbase-daemon.sh start regionserver
		ssh hadoop@master /home/hadoop/hbase/bin/hbase shell ~/git/physical_design/delete_table
		echo "sleeping for $SLEEP_TIME ..."
		sleep $SLEEP_TIME
	fi

	if $all || $create	
	then
		echo "creating usertable..."
		create_statement=$line	
		echo $create_statement > $RESULT_DIR/create_$counter.script
		echo "exit " >> $RESULT_DIR/create_$counter.script
 		scp $RESULT_DIR/create_$counter.script hadoop@master:$RESULT_DIR/create_$counter.script
		create_table $RESULT_DIR/create_$counter.script

		echo "sleeping for 10 sec ..."
		sleep $TEN
	fi

	if $all || $load
	then
		echo "loading data..."
		echo "starting time: " 
		echo `date +%s`
		./ld $number_of_records $number_of_threads `echo $RESULT_DIR/load_$counter.dat`
		echo "end time:"
		echo `date +%s`
		echo "sleeping for 10 sec ..."
		sleep $TEN
	fi

	if $all || $random_read
	then
        	echo "random read..."
        	echo "starting time: "
		echo `date +%s`
		./random_read $number_of_operations $number_of_threads `echo $RESULT_DIR/random_read_$counter.dat`
		echo "end time:"
		echo `date +%s`
		echo "sleeping for 10 sec ..."
		sleep $TEN
	fi

	if $all || $scan
	then
		echo "scan..."
		echo "start time: "
		echo `date +%s`
		./scan $number_of_operations $number_of_threads `echo $RESULT_DIR/scan_$counter.dat`
		echo "end time:"
		echo `date +%s`
		echo "sleeping for 10 sec ..."
		sleep $TEN
	fi

	if $all || $workloada
	then
		echo "workloada..."
		echo "start time: "
		echo `date +%s`
		./workloada $number_of_operations $number_of_threads `echo $RESULT_DIR/workloada_$counter.dat` $requestdistribution
		echo "end time:"
		echo `date +%s`
		echo "sleeping for 10 sec ..."
		sleep $TEN
	fi


	if $all || $workloadb
	then
		echo "workloadb..."
		echo "start time: "
		echo `date +%s`
		./workloadb $number_of_operations $number_of_threads `echo $RESULT_DIR/workloadb_$counter.dat`
		echo "end time:"
		echo `date +%s`
		echo "sleeping for 10 sec ..."
		sleep $TEN
	fi


	if $all || $workloadc
	then
		echo "workloadc..."
		echo "start time: "
		echo `date +%s`
		./workloadc $number_of_operations $number_of_threads `echo $RESULT_DIR/workloadc_$counter.dat`
		echo "end time:"
		echo `date +%s`
		echo "sleeping for 10 sec ..."
		sleep $TEN
	fi


	if $all || $workloadc1
	then
		echo "workloadc1..."
		echo "start time: "
		echo `date +%s`
		./workloadc1 $number_of_operations $number_of_threads `echo $RESULT_DIR/workloadc1_$counter.dat`
		echo "end time:"
		echo `date +%s`
		echo "sleeping for 10 sec ..."
		sleep $TEN
	fi


	let counter=$counter+1
done < $experiment_list_file

set +x
