#!/bin/bash

set -x

YCSB_DIR=/home/hadoop/ycsb-0.1.4
number_of_operations=100000
number_of_threads=20
number_of_records=10000000
output_file_suffix='.dat'
experiment_list_file=/home/hadoop/git/physical_design/experiments.list.withoutmajorcompaction
#experiment_list_file=/home/hadoop/git/physical_design/experiments.list
clean=false
create=false
load=false
random_read=false
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
	fi
done

let counter=1

function create_table {
	echo "creating table..."
	echo $1
	hbase shell $1
}


cd $YCSB_DIR
echo `pwd`

while read line
do
	if $all || $clean
	then
		echo "droping usertable..."
		hbase shell ~/git/physical_design/delete_table
		echo "sleeping for 10 sec..."
		sleep 10
	fi

	if $all || $create	
	then
		echo "creating usertable..."
		create_statement=$line	
		echo $create_statement > create_$counter.script
		echo "exit " >> create_$counter.script
		create_table create_$counter.script

		echo "sleeping for 10 sec"
		sleep 10
	fi

	if $all || $load
	then
		echo "loading data..."
		echo "starting time: " 
		echo `date +%s`
		./ld $number_of_records $number_of_threads `echo load_$counter.dat`
		echo "end time:"
		echo `date +%s`
	fi

	if $all || $random_read
	then
        	echo "random read..."
        	echo "starting time: "
		echo `date +%s`
		./random_read $number_of_operations $number_of_threads `echo random_read_$counter.dat`
		echo "end time:"
		echo `date +%s`
	fi

	if $all || $scan
	then
		echo "scan..."
		echo "start time: "
		echo `date +%s`
		./scan $number_of_operations $number_of_threads `echo scan_$counter.dat`
		echo "end time:"
		echo `date +%s`
	fi

	let counter=$counter+1
done < $experiment_list_file

set +x
