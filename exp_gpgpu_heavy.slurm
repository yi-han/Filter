#!/bin/bash
# Created by the University of Melbourne job script generator for SLURM
# Mon Dec 03 2018 07:51:58 GMT+1100 (Australian Eastern Daylight Time)

# Partition for the job:
#SBATCH --partition=gpgpu

# Multithreaded (SMP) job: must run on one node and the cloud partition
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
# The name of the job:
#SBATCH --job-name="heavyDDQNText"

# The project ID which this job should run under:
#SBATCH --account="punim0621"

# Maximum number of tasks/CPU cores used by the job:
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1

# The amount of memory in megabytes per process in the job:
#SBATCH --mem=25600

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

# Run the job from the directory where it was launched (default)

# The modules to load:
module load Tensorflow/1.8.0-intel-2017.u2-GCC-6.2.0-CUDA9-Python-3.5.2-GPU

# The job command(s):
time mpiexec -n 1 python3 runDDQN.py 0 2 "heavyDDQNText"