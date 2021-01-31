import h5py
import os 
import subprocess 
from osiris_suite import InputDeckManager 
import numpy as np 



hoffman_submission_script = '''
#!/bin/bash 
#$ -cwd
#$ -n hello! 
#$ -o output   # stdout redirect 
#$ -e err	# stderr redirect 
#$ -l highp,h_data=32G,h_rt=03:00:00,exclusive
#$ -V  # inherit all environment variables 
#$ -pe dc* %d

. /u/local/Modules/default/init/modules.sh


# reset output and error files 
echo "" > test_osiris.err
echo "" > test_osiris.out


# the below command indicates that at least 8 cpus are available on the node 
# cat /proc/cpuinfo

module unload intelmpi
module load hdf5/1.10.0-patch1_intel-17.0.1
module load intel/17.0.1
module load intelmpi
module load idl
module load ffmpeg 

echo "NSLOTS: " $NSLOTS 

# cat $PE_HOSTFILE | awk '{print $1}' | uniq > $TMPDIR/hostfile.$JOB_ID
# mpirun -f $TMPDIR/hostfile.$JOB_ID -ppn n executable-name

echo PE_HOSTFILE: $PE_HOSTFILE
cat $PE_HOSTFILE 

%s  

%s

'''

# create job submission script and execute 
def run_osiris_hoffman( osiris_bin_path, input_deck_path, 
		analysis_cmd = None,
		run_osiris = True, run_analysis = True ) :  

	deck = InputDeckManager( input_deck_path ) 

	# 2d 
	node_number = deck[ 'node_conf' ][ 'node_number(1:2)' ]

	num_nodes = np.product( node_number )

	sim_dir = os.path.dirname( os.path.abspath( input_deck_path ) )
	input_deck_basename = os.path.basename( input_deck_path )

	if osiris_bin_path and run_osiris : 
		osiris_cmd = 'mpirun -np $NSLOTS %s %s' % (
				osiris_bin_path, input_deck_basename)
	else : 
		osiris_cmd = '' 

	if not( analysis_cmd and run_analysis ) : 
		analysis_cmd = ''

	script = hoffman_submission_script % ( num_nodes, 
							osiris_cmd, analysis_cmd )

	script_path = sim_dir + '/submit.sh'

	with open( script_path, 'w' ) as f : 
		f.write( script )

	err = subprocess.Popen( 'qsub submit.sh', 
					shell = True, cwd = sim_dir ).wait() 

	return err 





recursive = 1 
step = 2 

# print all datasets 
def scan_hdf5( group ) : 
	
	for key, val in group.items():

		if isinstance(val, h5py.Dataset):
			# print(' ' * num_spaces + '---> ' + v.name)
			print( val.name )

		elif isinstance( val, h5py.Group ) :
			scan_hdf5( val ) 




def check_leaf_timesteps( data_arr ) : 

	# verify timesteps 
	success = 1 

	timesteps = None 

	# timesteps = data_arr[0].timesteps
	# indices = np.arange( len( timesteps ) )

	for leaf in data_arr : 
		
		try : 

			if timesteps is None : 
				timesteps = leaf.timesteps 

			success &= np.allclose( timesteps, leaf.timesteps ) 
		except : 
			pass  

	return success
