#!/bin/bash
rm -vf RUNDIR/*
echo "Making directory named test for the current run"
#mkdir RUNDIR
cp $1 RUNDIR/ -v
cd RUNDIR
echo "Run Starts"
echo "==============================================================================================" 
echo
echo
echo
nohup mpirun  -np $2 ./$1 $3 $4 &
#mpirun  -np $2 ./$1 $3 $4
