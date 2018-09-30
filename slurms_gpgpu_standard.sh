sbatch exp_gpgpu_single.slurm
sleep 5
sed 's/0 3/3 3/g' exp_gpgpu_single.slurm > output.slurm
sbatch output.slurm
sed 's/0 3/6 3/g' exp_gpgpu_single.slurm > output.slurm
sbatch output.slurm
sed 's/0 3/9 3/g' exp_gpgpu_single.slurm > output.slurm
sbatch output.slurm
sed 's/0 3/12 3/g' exp_gpgpu_single.slurm > output.slurm
sbatch output.slurm
sed 's/0 3/15 3/g' exp_gpgpu_single.slurm > output.slurm
sbatch output.slurm
sed 's/0 3/18 2/g' exp_gpgpu_single.slurm > output.slurm
sbatch output.slurm
