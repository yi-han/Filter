sed 's/runDDQN/runDDQN/g' exp_gpgpu_single.slurm > output.slurm
sed "s/samplePath/ddAdvGroup/g" output.slurm -i 
sed 's/sampleDDQNText/fbDdGroup/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/2 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runDDQNAdditional/g' exp_gpgpu_single.slurm > output.slurm
sed "s/samplePath/ddAdvSuperSplit/g" output.slurm -i 
sed 's/sampleDDQNText/fbDdSuper/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/2 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runDDQNHundred/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/sarAdvGroup/g" output.slurm -i 
sed 's/sampleDDQNText/fbSarGroup/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
sed 's/0 1/2 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runDDQNMalialis/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/sarAdvSuperSplit/g" output.slurm -i 
sed 's/sampleDDQNText/fbSarSuper/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
sed 's/0 1/2 1/g' output.slurm -i 
sbatch output.slurm