sed 's/runDDQN/runDDQNMalialis/g' exp_gpgpu_single.slurm > temp1.slurm
sed 's/sampleDDQNText/DDQNlaiHigh/g' temp1.slurm > temp2.slurm
sed 's/0 2/0 1/g' temp2.slurm > output.slurm
sbatch output.slurm
