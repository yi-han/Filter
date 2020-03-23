#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=7-00:00:00
#SBATCH --account=punim0636
#SBATCH --partition=physical
#SBATCH --job-name=sampleDDQNText
#SBATCH --mem=43000
# Send yourself an email when the job:
# aborts abnormally (fails)
#SBATCH --mail-type=FAIL
# ends successfully
#SBATCH --mail-type=END

# Use this email address:
#SBATCH --mail-user=jpattison@student.unimelb.edu.au

# Load required modules

# module load Python/3.6.4-intel-2017.u2-GCC-6.2.0-CUDA9
module load Tensorflow/1.3.0-intel-2017.u2-Python-3.5.2
# module load Tensorflow/1.1.0-intel-2016.u3-Python-3.5.2

# Launch multiple process python code

echo "Starting physical throttle"
time mpiexec -n 1 python3 runDDQN.py 0 2 "samplePath"

echo "done"


# my project file /data/projects/punim0621