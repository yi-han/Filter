sbatch exp_cloud.slurm
sleep 5
sed 's/0 5/5 5/g' exp_cloud.slurm > output.slurm
sbatch output.slurm
sed 's/0 5/10 5/g' exp_cloud.slurm > output.slurm
sbatch output.slurm
sed 's/0 5/15 5/g' exp_cloud.slurm > output.slurm
sbatch output.slurm