#!/bin/bash
#SBATCH --nodes 1
#SBATCH --partition gpgpu
#SBATCH --time=6-00:00:00
#SBATCH --cpus-per-task=1
#SBATCH --job-name=sampleDDQNText
#SBATCH --account=punim0621

#SBATCH --gres=gpu:1
#SBATCH --mem=10750


# Send yourself an email when the job:
# aborts abnormally (fails)
#SBATCH --mail-type=FAIL
# ends successfully
#SBATCH --mail-type=END
# Use this email address:
#SBATCH --mail-user=jpattison@student.unimelb.edu.au

# module load Tensorflow/1.8.0-intel-2017.u2-GCC-6.2.0-CUDA9-Python-3.5.2-GPU
# module load Theano/1.0.2-intel-2017.u2-Python-3.5.2-Tensorflow-1.10.0
# module load Python/3.5.2-goolf-2015a
module load Tensorflow/1.9.0-intel-2017.u2-GCC-6.2.0-CUDA9-Python-3.6.4-GPU

# Launch multiple process python code
# pip3 install --user scikit-learn



echo "Starting four throttle"
time mpiexec -n 1 python3 runDDQN.py 0 2 "samplePath"

echo "done"


# my project file /data/projects/punim0621