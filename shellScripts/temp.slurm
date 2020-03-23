#!/bin/bash
#SBATCH --nodes 1
#SBATCH --partition gpgpu
#SBATCH --time=5-00:00:00
#SBATCH --cpus-per-task=2
#SBATCH --job-name=DDQN100
#SBATCH --account=punim0621

#SBATCH --gres=gpu:1

module load Tensorflow/1.8.0-intel-2017.u2-GCC-6.2.0-CUDA9-Python-3.5.2-GPU

# module load Python/3.5.2-goolf-2015a

# Launch multiple process python code

echo "Starting four throttle"
time mpiexec -n 1 python3 runDDQN.py 0 2 "DDQN100"

echo "done"


# my project file /data/projects/punim0621
