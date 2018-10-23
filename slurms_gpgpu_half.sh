sed 's/0 2/0 1/g' exp_gpgpu_single.slurm > output.slurm
sbatch output.slurm
sleep 5
sed 's/0 2/1 1/g' exp_gpgpu_single.slurm > output.slurm
sbatch output.slurm
sed 's/0 2/2 1/g' exp_gpgpu_single.slurm > output.slurm
sbatch output.slurm
sed 's/0 2/3 1/g' exp_gpgpu_single.slurm > output.slurm
sbatch output.slurm
sed 's/0 2/4 1/g' exp_gpgpu_single.slurm > output.slurm
sbatch output.slurm
sed 's/0 2/5 1/g' exp_gpgpu_single.slurm > output.slurm
sbatch output.slurm
sed 's/0 2/6 1/g' exp_gpgpu_single.slurm > output.slurm
sbatch output.slurm
sed 's/0 2/7 1/g' exp_gpgpu_single.slurm > output.slurm
sbatch output.slurm
sed 's/0 2/8 1/g' exp_gpgpu_single.slurm > output.slurm
sbatch output.slurm
sed 's/0 2/9 1/g' exp_gpgpu_single.slurm > output.slurm
sbatch output.slurm
