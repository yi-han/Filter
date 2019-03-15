# exp3

sed 's/runDDQN/runSarsaY/g' exp_physical_ddqn.slurm > output.slurm
sed 's/sampleDDQNText/e3dd100SarSplitLong/g' output.slurm -i 
sed "s/samplePath/e3dd100SarSplitLong/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i 
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i 
sbatch output.slurm


sed 's/runDDQN/runSarsaZ/g' exp_physical_ddqn.slurm > output.slurm
sed 's/sampleDDQNText/e3sarSinDDSarSplitLong/g' output.slurm -i 
sed "s/samplePath/e3sarSinDDSarSplitLong/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i 
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i 
sbatch output.slurm
