#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=0-12:00:00
#SBATCH --partition=physical

# Load required modules
module load Python/3.5.2-goolf-2015a


# Launch multiple process python code

echo "Starting"
time mpiexec -n 1 python3 helloWorld.py

echo "done"


# my project file /data/projects/punim0621