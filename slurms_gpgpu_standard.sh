sbatch exp_gpgpu.slurm
sed 's/0 5/5 5/g' exp_gpgpu.slurm > output.slurm
sbatch output.slurm
sed 's/0 5/10 5/g' exp_gpgpu.slurm > output.slurm
sbatch output.slurm
sed 's/0 5/15 5/g' exp_gpgpu.slurm > output.slurm
sbatch output.slurm