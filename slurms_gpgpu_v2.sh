

sed 's/runDDQN/runSARSA/g' exp_gpgpu_single.slurm > output.slurm
sed "s/samplePath/DdAdvSuperEverything/g" output.slurm -i 
sed 's/sampleDDQNText/DdAdvSuperEverything/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm



sed 's/runDDQN/runSarsaAdditional/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/DdAdvGroupExtraAnnealing/g" output.slurm -i 
sed 's/sampleDDQNText/DdAdvGroupExtraAnnealing/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runSarsaDDQNCopy/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/DdAdvGroupLong/g" output.slurm -i 
sed 's/sampleDDQNText/DdAdvGroupLong/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runSarsaNoOverdrive/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/DdGroupAdvManyAction/g" output.slurm -i 
sed 's/sampleDDQNText/DdGroupAdvManyAction/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runSarsaOriginal/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/lowDdCentral/g" output.slurm -i 
sed 's/sampleDDQNText/lowDdCentral/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runSarsaX/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/DdGroupLowDiscount/g" output.slurm -i 
sed 's/sampleDDQNText/DdGroupLowDiscount/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runDDQNAdditional/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/DdGroupHighDiscount/g" output.slurm -i 
sed 's/sampleDDQNText/DdGroupHighDiscount/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runDDQNHundred/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/DdGenericSplit/g" output.slurm -i 
sed 's/sampleDDQNText/DdGenericSplit/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runDDQNMalialis/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/DdSplitLong/g" output.slurm -i 
sed 's/sampleDDQNText/DdSplitLong/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runDDQNNetQuick/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/ddSplitSuper/g" output.slurm -i 
sed 's/sampleDDQNText/ddSplitSuper/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runSarsaY/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/ddSuperLong/g" output.slurm -i 
sed 's/sampleDDQNText/ddSuperLong/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm


