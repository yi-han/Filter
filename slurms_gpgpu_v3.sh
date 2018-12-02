sed 's/runDDQN/runDDQNNetQuick/g' exp_gpgpu_single.slurm > temp1.slurm
sed 's/sampleDDQNText/DDFour/g' temp1.slurm > temp2.slurm
sed 's/0 2/0 2/g' temp2.slurm > output.slurm
sbatch output.slurm
