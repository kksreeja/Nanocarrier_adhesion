#!/bin/bash 
#PBS -N abc
#PBS -M kksreej@gmail.com 
#PBS -o output.dat
#PBS -l nodes=1:ppn=1
#PBS -l walltime=500:00:00

cd $PBS_O_WORKDIR
echo $PBS_JOBID >job_details.dat
echo "starting time: ">>job_details.dat
date >>job_details.dat
module load openmpi-2.1.1-icc
#jobid=`echo $PBS_JOBID | cut -f1 -d '.'` 
#rundir=/scratch-local/job-$jobid 
#echo "name of rundir is $rundir" >>job_details.dat 
#mkdir -pv $rundir 
#mv Makefile ./CC_SOURCE ./CC_INCLUDE ./FC_SOURCE ./FC_INCLUDE ./RUNDIR ./PARAMETERS ./SYS_STATE $rundir 
#cd $rundir 
make clean
make
cp free_ener ./RUNDIR
cd ./RUNDIR
mpirun -np 1 ./free_ener false nodebug dump  
#cd ../
#mv * $PBS_O_WORKDIR 
#cd ../
#rmdir $rundir 
