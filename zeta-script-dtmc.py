def make_directories(cwd):
	print (cwd)
        
	os.mkdir(cwd+'/PARAMETERS')
	os.mkdir(cwd+'/RUNDIR')
	os.mkdir(cwd+'/SYS_STATE')
	os.mkdir(cwd+'/SYS_STATE/MEMB')
	os.mkdir(cwd+'/SYS_STATE/NC-DATA')
	os.mkdir(cwd+'/SYS_STATE/ANTIGEN')		
	os.mkdir(cwd+'/SYS_STATE/DUMP')
	os.mkdir(cwd+'/SYS_STATE/RESTART')
	os.mkdir(cwd+'/SYS_STATE/SYSTEM')

def system_parameters(parameter):
	fp=open('./PARAMETERS/system-parameters.inp','w')
	for f in parameter:		
		fp.write(str(f[0])+', '+str(f[1])+'\n')
	fp.close()

def membrane_parameters(parameter):
	fp=open('./PARAMETERS/membrane_parameters.inp','w')
	for f in parameter:
		fp.write(str(f[0])+'   '+str(f[1])+'\n')
	fp.close()

def nc_parameters(ncno,param):
	ab,nc,bias=param
	filename='./PARAMETERS/nc-'+str(ncno)+'.ncinp'
	fp =  open(filename,'w')
	fp.write('<antibody>\n')
	fp.write('ab_type, '+str(ab[0])+'\n')
	fp.write('ab_radius, ')
	for i in range(ab[0]-1):
		fp.write(str(ab[1][i])+',')
	fp.write(str(ab[1][-1])+'\n')
	fp.write('ab_length, ')
	for i in range(ab[0]-1):
		fp.write(str(ab[2][i])+',')
	fp.write(str(ab[2][-1])+'\n')
	fp.write('</antibody>\n\n')
	
	fp.write('<nanocarrier>\n')
	fp.write('nc_shape, '+str(nc[0])+'\n')
	fp.write('nc_radius, '+str(nc[1])+'\n')
	fp.write('nc_num_ab, '+str(nc[2])+'\n')
	fp.write('nc_rstart, '+str(nc[3])+'\n')
	fp.write('nc_hstart, '+str(nc[4])+'\n')
	
	fp.write('ab_type_conc, ')
	for i in range(ab[0]-1):
		fp.write(str(nc[5][i])+',')
	
	fp.write(str(nc[5][-1])+'\n')
	fp.write('ab_mode, '+str(nc[6])+'\n')
	fp.write('</nanocarrier>\n\n')
	
	
	fp.write('<bias>\n')
	fp.write('bias_mode, '+str(bias[0])+'\n')
	fp.write('biasstrength, '+str(bias[1])+'\n')
	fp.write('biasref, '+str(bias[2])+'\n')
	fp.write('binsize, '+str(bias[3])+'\n')
	fp.write('biasdir, '+str(bias[4])+'\n')
	fp.write('TI_lambda, '+str(bias[5])+'\n')
	fp.write('</bias>\n\n')
	fp.close()

def interaction_parameters(nab,nrec,kspr,delg):
	filename='./PARAMETERS/int_param.inp'
	fp =  open(filename,'w')
	fp.write('<kbond>\n')
	for i in range(nab):
		for j in range(nrec):
			fp.write(str(i)+','+str(j)+','+str(kspr[i][j])+'\n')
	fp.write('</kbond>\n\n')
	
	fp.write('<delg>\n')
	for i in range(nab):
		for j in range(nrec):
			fp.write(str(i)+','+str(j)+','+str(delg[i][j])+'\n')
	fp.write('</delg>\n\n')
	fp.close()
	
def antigen_parameters(param):
	filename='./PARAMETERS/antigen_parameters.inp'
	fp =  open(filename,'w')
	fp.write('<total>\n')
	fp.write('N, '+str(param[0])+'\n')
	fp.write('</total>\n')
	fp.write('<pattern>\n')
	fp.write('pat, '+str(param[1])+'\n')
	fp.write('</pattern>\n')
	fp.write('<type>\n')
	fp.write('n, '+str(param[2])+'\n')
	fp.write('</type>\n')
	
	fp.write('<conc>\n')
	for i in range(param[2]):
	    fp.write(str(i)+', '+str(param[3][i])+'\n')
	fp.write('</conc>\n')
	
	fp.write('<radius>\n')
	for i in range(param[2]):
	    fp.write(str(i)+', '+str(param[4][i])+'\n')
	fp.write('</radius>\n')
	fp.write('<length>\n')
	for i in range(param[2]):
	    fp.write(str(i)+', '+str(param[5][i])+'\n')
	fp.write('</length>\n')
	fp.write('<flexure>\n')
	for i in range(param[2]):
	    fp.write(str(i)+', '+str(param[6][i])+'\n')
	fp.write('</flexure>\n')
	fp.close()

#!/bin/env python
import numpy,sys,os,time,shutil,stat,subprocess,glob,random
start_ens,end_ens = int(sys.argv[1]),int(sys.argv[2])

if len(sys.argv) <3:
	print 'Enter the number for starting and ending ensembles'
	sys.exit('Exiting')
	
n_processor=1

benergy={'SB':-7.9108E-20, 'IB':-5.1565E-20,'WB':-0.75629E-20}
zstartdict={'approach':[84.6],'recede':[79.5]}

source_dir=os.getcwd()

# NC definition
num_nc = 1
nc_shapes=['sphere']
nc_radii=[50.0]
nc_num_abs=[162]
nc_rstarts=[84.5]
nc_hstarts=[0.0]
ab_type_concs=[[1.0]]
ab_modes=['random']

#bias
bias_modes=['N']
bias_strengths=[1.0]
biasrefs=[84.5]
binsizes=[0.1]
biasdirs=['approach']
TI_lambdas=[1.0]

#abdata
abtype=1
ab_radii=[1.5]
ab_length=[15.0]
abparam=[abtype,ab_radii,ab_length]

#antigen
anttype = 1
ant_density  = 0.002                                          # 0.002 -> 2000 antigens per micron^2
antpat = 'random'
antconcs = [1.0]
antradii = [1.5]
antlengths = [19.0]
antflexures = [7000]

#interaction parameters
kspr={0:{0:1.0}}
delg={0:{0:0.0}}

#C++ variables
num_mc_moves=5000000
cpp_param=[['pbchoverl',1.0],
['num_nanocarriers',1],
['memb_lattice_size',49],
['memb_lattice_space',5.0],
['temperature',300],
['run_system','membrane_DTMC'],
['mpi_mode','serial'],
['win_start',0],
['win_end',1],
['num_mc_moves',num_mc_moves],
['num_dtmc_moves',num_mc_moves],
['osd_print_interval',int(num_mc_moves/10000)],
['sampling_interval',int(num_mc_moves/10000)],
['window_antab_data_interval',int(num_mc_moves/10000)],
['window_conf_interval',int(num_mc_moves/500)],
['antigen_memb_write_interval',int(num_mc_moves/1000)],
['binsize_rdf',1.0]]

restart_memb = False
fort_param=[
[20,"!Bending Rigidity"],
[0.0 ,"!czero"],
['CIRCULAR' ,"!czero_pattern"],
[0.0 ,"!czero_conc"],
[4 ,"!annulus_start_ring"],
[10 ,"!annulus_end_ring"],
[0.0,"!pressure"],
['PLANAR',"!System_Geom"],
[20,"!Sinusoidal height"],
[2,"!Periodicity"],
[1.0,"!blen_scale_factor"],
['.False.',0],
['.False.',"!antigen_restart_flag"],
[20000,"!datainterval"],
['.False.',"! is the frame fixed or not ?"],
[2.0,"! shadow_size"]]

num_antigens=int((cpp_param[3][1]*(1+cpp_param[2][1]))**2*ant_density)    # computed from the density predefined in the system (2000 antigens per micron^2)

kappaval = [20]                           
nab=162
num_antibody = [nab]

startconf_dir=source_dir+'/../..'
codehome=os.getcwd()
exec_name='free_ener'

for bls in [10.0]:
    cpp_param[3][1]=bls
    blen_fac=[bls-bls*0.975,bls-bls*0.95,bls-bls*0.825]
    boxheight = (cpp_param[2][1]+1)*bls*cpp_param[0][1]
    
    run_prefix='Membrane-N-'
    dirname1=run_prefix+str(cpp_param[2][1]+1)+"_bl-"+str(bls)
    dirname1_rs=source_dir+'/run1/Membrane-N-'+str(cpp_param[2][1]+1)+'_bl-'+str(bls)
    subprocess.call(["mkdir","-pv",dirname1])
    os.chdir(dirname1)
    
    curdir_out=os.getcwd()
    
    for blen_scale_factor in blen_fac:
        fort_param[10][0]=blen_scale_factor     #set the correct value in the fortran parameter list
        dirname10='blen-scale-factor-'+str(blen_scale_factor)
        subprocess.call(["mkdir","-pv",dirname10])
        os.chdir(dirname10)
       	        		        		
        kappadir=os.getcwd()
        for kappa in kappaval:
            fort_param[0][0]=kappa
            dirname40='kappa-'+str(kappa)
            subprocess.call(["mkdir","-pv",dirname40])
            os.chdir(dirname40)
            curdir=os.getcwd()
            for ens in range(start_ens,end_ens):     
                run_exe='DTMC-'+str(int(bls))+'-'+str(kappa)+'-'+str(blen_scale_factor)+'-'+str(ens)
                dirname5='ENS-'+str(ens)
                subprocess.call(["mkdir","-pv",dirname5])
                os.chdir(dirname5)  
                memb_restart,res_file_num=".False.",0
    
                if restart_memb:    
                    restart_dir1=dirname1_rs+'/'+dirname10+'/'+dirname40
                    restartdata=glob.glob(restart_dir1+'/ENS*')
		    print(restart_dir1)
                    randomens=random.randint(0,len(restartdata)-1)
                    restart_dir=restartdata[randomens]+'/SYS_STATE/DUMP'
                    print restart_dir
                    dumplist=glob.glob(restart_dir+'/*.dump')
                    memb_restart,memb_res_file=".True.",dumplist[random.randint(0,len(dumplist)-1)]
                    res_file_num=int(memb_res_file.split('.dump')[0].split('-')[-1])
                    print memb_restart,memb_res_file
                    fort_param[11][0]='.True.'
                    fort_param[11][1]=res_file_num
    
        	make_directories(os.getcwd())
                system_parameters(cpp_param)
                membrane_parameters(fort_param)
    
                for i in range(num_nc):
                    ncparam = [nc_shapes[i],nc_radii[i],nc_num_abs[i],boxheight-2*nc_rstarts[i],nc_hstarts[i],ab_type_concs[i],ab_modes[i]]
                    biasparam = [bias_modes[i],bias_strengths[i],biasrefs[i],binsizes[i],biasdirs[i],TI_lambdas[i]]
                    nc_parameters(i,[abparam,ncparam,biasparam])
                interaction_parameters(abtype,anttype,kspr,delg)
                antigen_parameters([num_antigens,antpat,anttype,antconcs,antradii,antlengths,antflexures])
                shutil.copyfile(codehome+'/'+exec_name,'RUNDIR/'+run_exe)
                shutil.copytree(codehome+'/PARAMETERS/SPH_RAD1_'+str(nab),'./PARAMETERS/SPH_RAD1_'+str(nab))
                shutil.copyfile(codehome+'/PARAMETERS/sphere'+str(nab)+'.in','./PARAMETERS/sphere'+str(nab)+'.in')
                if restart_memb==1:
                    shutil.copyfile(memb_res_file,'./SYS_STATE/RESTART/membrane_state-'+str(res_file_num)+'.dump')
          	os.chdir('./RUNDIR')
                os.chmod(run_exe,stat.S_IRWXU)
    
          	fp=open('subscript.sh','w')
                fp.write("#!/bin/bash"+'\n')
                fp.write("module load mpich/3.2/gcc"+"\n")
                fp.write("nohup mpirun -np "+str(n_processor)+" ./"+str(run_exe)+'  false  debug \n')
                fp.close()
                runcmd="bash subscript.sh &"
                os.system(runcmd)
                os.chdir(curdir)
            os.chdir(kappadir)
        os.chdir(curdir_out)
    os.chdir(source_dir)
