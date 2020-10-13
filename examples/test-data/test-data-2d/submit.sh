#!/bin/bash 
#$ -cwd
#$ -o test_osiris.out   # stdout redirect 
#$ -e test_osiris.err	# stderr redirect 
#$ -l highp,h_data=16G,h_rt=00:15:00,exclusive
#$ -V  # inherit all environment variables 
#$ -pe dc* 1

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

echo "NSLOTS: " $NSLOTS 


osiris_bin=$OSIRIS_FORK_BIN_PATH/osiris-2D-dev.e 


# cat $PE_HOSTFILE | awk '{print $1}' | uniq > $TMPDIR/hostfile.$JOB_ID
# mpirun -f $TMPDIR/hostfile.$JOB_ID -ppn n executable-name

echo PE_HOSTFILE: $PE_HOSTFILE
cat $PE_HOSTFILE 


# mpirun $osiris input
mpirun -np $NSLOTS $osiris_bin input.os
# mpirun -print-rank-map -np $NSLOTS -ppn 8 $osiris os-input
# mpirun -print-rank-map -ppn 8 $osiris os-input


