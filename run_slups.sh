sbatch exp_one_node_one_core
sed 's/0 10/10 10/g' exp_one_node_one_core.slurm > output.slurm
sbatch output.slurm
