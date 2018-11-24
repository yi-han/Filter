#!/bin/bash
# Created by the University of Melbourne job script generator for SLURM
# Fri Nov 23 2018 14:12:05 GMT+1100 (Australian Eastern Daylight Time)

# Partition for the job:
#SBATCH --partition=physical

# Multithreaded (SMP) job: must run on one node and the cloud partition
#SBATCH --nodes=1

# The name of the job:
#SBATCH --job-name="sampleDDQNText"

# The project ID which this job should run under:
#SBATCH --account="punim0636"

# Maximum number of tasks/CPU cores used by the job:
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1

# Send yourself an email when the job:
# aborts abnormally (fails)
#SBATCH --mail-type=FAIL
# ends successfully
#SBATCH --mail-type=END

# Use this email address:
#SBATCH --mail-user=jpattison@student.unimelb.edu.au

# The maximum running time of the job in days-hours:mins:sec
#SBATCH --time=5-0:0:00

# check that the script is launched with sbatch
if [ "x$SLURM_JOB_ID" == "x" ]; then
   echo "You need to submit your job to the queuing system with sbatch"
   exit 1
fi

# Run the job from this directory:
cd /data/projects/punim0636/

# The modules to load:
module load Tensorflow/1.3.0-intel-2017.u2-Python-3.5.2

# The job command(s):
time mpiexec -n 1 python3 runDDQN.py 0 2 "sampleDDQNText"