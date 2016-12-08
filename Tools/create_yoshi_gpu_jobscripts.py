#!/usr/bin/env python

# !!IMPORTANT!! When not running tests, last PRINTED line should NOT be a comment (it's a "cp" command to copy the whole simulations folder)

import os
import math
import fnmatch # for filtering the file list to get the top,gro,mdp,ndx files.


N = 5  # NUMBER OF SCRIPTS TO SUBMIT = total time running will be this number times the Walltime

Walltime = '200:00:00'  # Walltime in format 'h:mm:ss'
SimTime = 200   # maximum run length of simulation in hours, it can be also a fraction of an hour

Email = 'laila.e@fu-berlin.de'

#NodesNum =  2 
Cpus = 8  # soroban = 12 cpus/node ; sheldon-ng = 8 cpus/node
Memory = 2048
#SimLen = 60000  # total simulation time length in ps
Partition = 'main' # use 'test' for testing and 'main' otherwise 

#next 3 lines only useful when running also grompp
#IndexFile = ' 'mpi for one node
#FirstGro = 'sam17_water216'
#FirstMdp = 'Mini.mdp'


Simns = {216:60, 1000:60, 2000:60, 3000:60, 4000:60, 5000:60, 6500:60, 7000:80, 8000:80, 9000:80, 10000:100}  # total simulation time length in ns
Nodes = {1000:1, 2000:1, 3000:1, 4000:1, 5000:1, 6500:1, 7000:1, 8000:1, 9000:1, 10000:1}  # 1 node
#Nodes = {1000:2, 2000:2, 3000:2, 4000:2, 5000:2, 6500:2, 7000:2, 8000:2, 9000:2, 10000:2} # 2 nodes
# old Nodes = {216:2, 1000:3, 2000:3, 3000:3, 4000:3, 5000:3, 6500:3, 7000:5, 8000:6, 9000:6, 10000:6} 

pc = [11]  # For testing
molec = [9000] #For testing

#pc = [0, 11, 22, 33, 37, 44, 50]
#molec = [1000, 2000, 3000, 4000, 5000, 6500, 7000, 8000, 9000, 10000]


BackupDir = '/home/eixeres/Version_v2/FINISHED'   # directory to copy (backup) simulation output
# old BackupDir = '/home/eixeres/Dec14_Last_Sims/FINISHED/'==>>> mpi for one node


for i in pc:
	for j in molec:
	  
		SimLen = Simns[j]*1000  # total simulation time length in ps
		NodesNum = Nodes[j]
		CpuNum = NodesNum*Cpus
		#N = Simns[j]  # NUMBER OF SCRIPTS TO SUBMIT
		
		# old Dir = '/Volumes/Backup/YosemiteFiles/MEGAsync/scripts/Python/SCRIPT_CREATION/sheldon-ng/s'+str(i)+'_w'+str(j)
		#Dir = '/Volumes/Backup/YosemiteFiles/Dropbox/Dropbox/scripts/Python/SCRIPT_CREATION/sheldon-ng/s'+str(i)+'_w'+str(j)+'/1node'
		#Dir = '/home/eixeres/Downloads/SCRIPTS_JOBS_NewVersion4/' + str(NodesNum) + 'node'+'/s'+str(i)+'_w'+str(j)
		#Dir = '/Users/burbol2/Downloads/SCRIPTS_JOBS_NewVersion4/' + str(NodesNum) + 'node'+'/s'+str(i)+'_w'+str(j)
		#Dir = '/Users/eixeres/Dropbox/GitHub/LineTensionPackage/Tools/SubmissionScripts/' + str(NodesNum) + 'node'+'/s'+str(i)+'_w'+str(j)
		DirNode = '/Users/eixeres/Dropbox/GitHub/LineTensionPackage/Tools/SubmissionScripts/' + str(NodesNum) + 'node' # main local directory where scripts using same number of nodes will be saved 

		if not os.path.exists(DirNode):
			os.system("mkdir "+ DirNode)
		Dir = DirNode +'/s'+str(i)+'_w'+str(j)
		
		SimDir = '/scratch/eixeres/Version_v2/s'+str(i)+'_w'+str(j)   #directory from where to run simulation
		Filename = 'NVT_sam'+str(i)+'_water'+str(j)  # name of files #===>>>> WHY 2 DIFF. VARIABLES?? Filename and NVTfile??
		Scriptname = str(NodesNum) + 'n_s'+str(i)+'_w'+str(j)  # name of script (when NOT testing, set equal to "Filename")??
		
		Startfile='sam'+str(i)+'_water'+str(j)
		Minifile='Mini_sam'+str(i)+'_water'+str(j)
		NVTfile = 'NVT_sam'+str(i)+'_water'+str(j)
		topfile= str(i)+'pc_'+str(j)+'.top'
		Minimdp = 'Mini_v2.mdp'
		NVTmdp = 'NVT_'+str(Simns[j])+'ns_v2.mdp'
	
		os.system("mkdir "+ Dir)
		for k in range(N):
		
			Jobname = str(NodesNum) +'n_'+str(i)+'_'+str(j)+ '_'+str(k)  # Name of job
			JobOut = open(Dir + '/' + Scriptname +'_'+ str(k),'w')
			JobOut.write('#!/bin/bash\n')
			JobOut.write('\n')
			JobOut.write('#SBATCH -p '+ Partition +'\n')
			JobOut.write('\n')
			JobOut.write('#SBATCH --mem=' + str(Memory) +'\n')
			JobOut.write('#SBATCH --job-name=' + Jobname + '\n')
			JobOut.write('#SBATCH --output=' + Scriptname + '_' + str(k) + '.out\n')
			JobOut.write('\n')
			JobOut.write('#SBATCH --mail-user=' + Email + '\n')
			JobOut.write('#SBATCH --mail-type=end\n')
			JobOut.write('#SBATCH --mail-type=fail\n')
			JobOut.write('\n')
			#JobOut.write('#SBATCH --ntasks=' + str(CpuNum)+'\n')
			JobOut.write('#SBATCH --tasks-per-node=' + str(Cpus)+'\n')
			JobOut.write('#SBATCH --nodes=' + str(NodesNum) +'\n')
			#JobOut.write('#SBATCH --exclusive')  # we want to run on only 1 node
			JobOut.write('\n')
			JobOut.write('#SBATCH --time=' + Walltime  + '\n')
			JobOut.write('\n')
			JobOut.write('module load slurm \n')
			JobOut.write('\n')
			JobOut.write('module load gromacs/single/2016\n')
			JobOut.write('\n')
			JobOut.write('STARTTIME=$(date +%s)\n' + '\n')
			JobOut.write('\n')
			JobOut.write('cd ' + SimDir + '\n')
			JobOut.write('\n')

			if k == 0:
				JobOut.write('gmx grompp -f ' + Minimdp + ' -c ' + Startfile + '.gro -p ' + topfile + ' -o '+ Minifile +'.tpr -maxwarn 9\n')
				
				# For more then 1 node use mpirun
				#JobOut.write('mpirun -np ' + str(CpuNum) + ' mdrun -deffnm ' + Minifile + ' -maxh ' + str(SimTime) + ' -v \n')

				# For only 1 node mpi not needed:
				JobOut.write(' mdrun -deffnm ' + Minifile + ' -maxh ' + str(SimTime) + ' -v \n')
				
				JobOut.write('gmx grompp -f ' + NVTmdp + ' -c ' + Minifile + '.gro -p ' + topfile + ' -o '+ NVTfile +'.tpr -maxwarn 9\n')

				#first jobscript changes "mdp" options with tpbconv to extend simulation
				#JobOut.write('tpbconv -s ' + Filename + '.tpr  -until ' + str(SimLen) + ' -o ' + Filename + '.tpr \n')
				
				JobOut.write('\n')
				
				# For more then 1 node use mpirun
				#JobOut.write('mpirun -np ' + str(CpuNum) + ' mdrun -s ' + Filename + '.tpr -deffnm  '+ Filename + ' -maxh ' + str(SimTime) + ' -v \n')
				
				# For only 1 node mpi not needed:
				JobOut.write(' mdrun -s ' + Filename + '.tpr -deffnm  '+ Filename + ' -maxh ' + str(SimTime) + ' -v \n')

			else:
				JobOut.write('mpirun -np ' + str(CpuNum) + ' mdrun -cpi '+ Filename + '.cpt -s ' + Filename + '.tpr -deffnm  '+ Filename + ' -maxh ' +
					str(SimTime) + ' -v \n')			

			JobOut.write('\n')	
			
			if k < N-1: # note that we count from 0 to N-1, so the 50th jobscript has i = 49
				
				# first N-1 jobscripts check if runtime is less then 15 sec, if not, submit next script 
				JobOut.write( 'RUNTIME=$(($(date +%s)-$STARTTIME))\n' + '\n'+ 'echo \"the job took $RUNTIME seconds...\"\n' + '\n' + 'if [[ $RUNTIME -lt 10 ]]; then\n' +

							'   echo "job took less than 10 seconds to run, aborting."\n' + '   exit\n' + 'else\n' + '   echo "everything fine..."\n' + '   sbatch ' + Scriptname +'_'+ str(k+1) + '\n') 
				JobOut.write('   fi\n')
				JobOut.write('\n')	
					
			# after the last run, we also want to backup the simulation files
			elif k == N-1:
				#JobOut.write("mkdir " + BackupDir + '\n')
				JobOut.write('cp -r ' + SimDir + ' ' + BackupDir + '\n')
				
			JobOut.close()



