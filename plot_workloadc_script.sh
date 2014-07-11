#!/bin/bash

let counter=0

for i in `seq 34 3 63`
do
	let counter=$counter+1
	let j=$i+1
	let z=$j+1
	echo "python3 plot_workloadc.py  -caseresult_dir caseresult -cases $i:$j:$z -loc 0 -title Run$counter > plot_workloadc$i$j$z.dat"
	python3 plot_workloadc.py  -caseresult_dir caseresult -cases "$i:$j:$z" -loc 0 -title "Run$counter" > "plot_workloadc$i$j$z.dat"

done
