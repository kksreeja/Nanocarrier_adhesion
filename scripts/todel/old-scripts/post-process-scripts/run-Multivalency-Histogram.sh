#!/bin/bash
script_dir=`pwd`
script_name='Make-Multivalency-Histogram.py'
filename='Multivalency-ENS-0_Frame-1.dat'
cd $1
for d1 in blen*/
do
	cd $d1
	for d2 in Flex*/
	do
		cd $d2
		for d3 in */
		do
			cd $d3
			for d4 in zstart*/
			do
				cd $d4
				for d5 in AB*/
				do
					cd $d5
					pwd
					cp -vf $script_dir/$script_name .
					python $script_name $filename
					rm -vf $script_name
					cd ../ #d5
					done
				cd ../ #d4
			done
			cd ../ #d3
		done
		cd .. #d2 
	done
	cd ..  #d1
done

