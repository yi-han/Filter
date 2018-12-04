sed 's/runDDQN/runDDQNHundred/g' exp_gpgpu_heavy.slurm > temp1.slurm
sed 's/heavyDDQNText/DDsever/g' temp1.slurm > temp2.slurm
sed 's/0 2/0 1/g' temp2.slurm > output.slurm
sbatch output.slurm
