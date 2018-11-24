#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=5-00:00:00
#SBATCH --account=punim0636
#SBATCH --partition=physical
#SBATCH --job-name=sample_sarsa_name
# Load required modules

module load Python/3.6.4-intel-2017.u2-GCC-6.2.0-CUDA9


# Launch multiple process python code

echo "Starting physical throttle"
time mpiexec -n 1 python3 runSARSA.py 0 5 "sample_sarsa_name"

echo "done"


# my project file /data/projects/punim0621