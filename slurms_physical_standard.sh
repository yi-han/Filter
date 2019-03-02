sed 's/runDDQN/grid_test/g' exp_physical.slurm > output.slurm
sed "s/samplePath/$1/g" output.slurm -i 
sed 's/sampleDDQNText/grid_small/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runDDQNAdditional/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/$1/g" output.slurm -i 
sed 's/sampleDDQNText/grid_mid/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm


sed 's/runDDQN/runSARSA/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/$1/g" output.slurm -i 
sed 's/sampleDDQNText/grid_64/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm

