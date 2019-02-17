# Using this for comparing differnt advesary groups against 


#sed 's/runDDQN/runDDQN/g' exp_gpgpu_single.slurm > output.slurm
sed 's/runDDQN/runDDQN/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/sarsMidHierAdvGroup/g" output.slurm -i
sed 's/sampleDDQNText/advGroup/g' output.slurm -i
# sbatch output.slurm
# sleep 5
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runDDQNAdditional/g' output.slurm -i
sed 's/advGroup/advSplit/g' output.slurm -i
sed "s/sarsMidHierAdvGroup/sarsMidHierAdvSplit/g" output.slurm -i
sed 's/1 1/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQNAdditional/runDDQNHundred/g' output.slurm -i
sed 's/advSplit/advShare/g' output.slurm -i
sed 's/sarsMidHierAdvSplit/sarsMidHierAdvSplitShare/g' output.slurm -i
sed 's/1 1/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm


