# exp3 tests

sed 's/runDDQN/runSarsaY/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/e3dd100SarSplitLong/g' output.slurm -i 
sed "s/samplePath/e3dd100SarSplitLong/g" output.slurm -i 
sed 's/0 2/0 4/g' output.slurm -i 
sbatch output.slurm



sed 's/runDDQN/runSarsaZ/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/e3sarSinDDSarSplitLong/g' output.slurm -i 
sed "s/samplePath/e3sarSinDDSarSplitLong/g" output.slurm -i 
sed 's/0 2/0 4/g' output.slurm -i 
sbatch output.slurm
