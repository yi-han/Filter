#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=0-12:00:00
#SBATCH --account=punim0636
#SBATCH --partition=physical
#SBATCH --job-name=sarsa_throttle
# Load required modules

module load Python/3.5.2-goolf-2015a


# Launch multiple process python code

echo "Starting physical throttle"
time mpiexec -n 1 python3 runSARSA.py 0 1

echo "done"


# my project file /data/projects/punim0621