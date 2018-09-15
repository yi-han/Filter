#!/bin/bash
#SBATCH --nodes 2
#SBATCH --ntasks-per-node=1
#SBATCH --partition gpgpu
#SBATCH --gres=gpu:p100:1
#SBATCH --time 08:00:00
#SBATCH --cpus-per-task=1
#SBATCH --job-name=dual_router_throttle

module load Tensorflow/1.8.0-intel-2017.u2-GCC-6.2.0-CUDA9-Python-3.5.2-GPU

# Launch multiple process python code

echo "starting parrelel process 0 1"
time mpiexec srun python3 run_multi_core.py 5 3

echo "Starting sarsacentralised big Spartan 1 1"
time mpiexec python3 run_multi_core.py 1 1

echo "done"


# my project file /data/projects/punim0621