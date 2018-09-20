sbatch exp_one_node_one_core.slurm
sed 's/0 5/5 5/g' exp_one_node_one_core.slurm > output.slurm
sbatch output.slurm
sed 's/0 5/10 5/g' exp_one_node_one_core.slurm > output.slurm
sbatch output.slurm
sed 's/0 5/15 5/g' exp_one_node_one_core.slurm > output.slurm
sbatch output.slurm