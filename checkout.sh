#! /bin/bash

for i in `seq 1 401`
do 
	git checkout case`echo $i`.list
done
