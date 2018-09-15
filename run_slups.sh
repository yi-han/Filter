sed 's/0 4/4 4/g' exp_one_node_one_core.slurm > output.slurm
sbatch exp_one_node_one_core.slurm
sbatch output.slurm
sed 's/0 4/8 4/g' exp_one_node_one_core.slurm > output.slurm
sbatch output.slurm