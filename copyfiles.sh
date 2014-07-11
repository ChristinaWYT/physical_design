#!/bin/bash
let count=$3
for i in `seq $1 $2`
do
	cp case`echo $i`.list case`echo $count`.list
	let count=$count+1
done
