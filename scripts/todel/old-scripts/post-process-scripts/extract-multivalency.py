#!/bin/env python
import numpy,os,sys,glob
title,data=[],[]
title.append('#Multivalency')
filename='Avg-Multivalency-ENS-0_Frame-1.dat'
flex=glob.glob('Flex*')
dir1=os.getcwd()
for fl in flex:
	os.chdir(fl)
	os.chdir('./PLANAR/zstart-0.0/')
	kappa=glob.glob('kappa*')
	print kappa
	for k in kappa:
		dir2=os.getcwd()
		os.chdir(k)
		abody=glob.glob('AB*')
		for ab in abody:
			t1='#'+fl.split('-')[1]+str(k)+'-ab-'+ab.split('-')[1]
			title.append(t1)
			d1=numpy.loadtxt(ab+'/'+filename)
			d2,d3=d1[:,0],d1[:,2]
			print
			print t1
			data.append(d3)
			print d3
		os.chdir(dir2)
	os.chdir(dir1)

outfile='./Multivalency-data-combined.dat'
fp=open(outfile,'w')
for i in range(0,title.__len__()-1):
	fp.write(title[i]+',')
fp.write(title[-1]+'\n')

for i in range(0,d2.__len__()):
	fp.write(str(d2[i])+',')
	for j in range(0,data.__len__()-1):
		fp.write(str(data[j][i])+',')
	fp.write(str(data[-1][i])+'\n')
fp.close()



