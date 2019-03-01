# 
# sed 's/runDDQN/runDDQN/g' exp_physical_ddqn.slurm > output.slurm
# sed "s/samplePath/$1/g" output.slurm -i 
# sed 's/sampleDDQNText/dRandomSingle/g' output.slurm -i 
# sed 's/0 2/0 2/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm

sed 's/runDDQN/runSARSA/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/sGroupShort/g" output.slurm -i 
sed 's/sampleDDQNText/sGroupShort/g' output.slurm -i 
sed 's/0 2/0 2/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm


sed 's/runDDQN/runSarsaAdditional/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/sSplitShort/g" output.slurm -i 
sed 's/sampleDDQNText/sSplitShort/g' output.slurm -i 
sed 's/0 2/0 2/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

# sed 's/runDDQN/runSarsaDDQNCopy/g' exp_physical_ddqn.slurm > output.slurm
# sed "s/samplePath/sSar100AdvGroup/g" output.slurm -i 
# sed 's/sampleDDQNText/sSar100AdvGroup/g' output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm

# sed 's/runDDQN/runSarsaNoOverdrive/g' exp_physical_ddqn.slurm > output.slurm
# sed "s/samplePath/sSar100AdvSuper/g" output.slurm -i 
# sed 's/sampleDDQNText/sSar100AdvSuper/g' output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm

# sed 's/runDDQN/runDDQNNetQuick/g' exp_physical_ddqn.slurm > output.slurm
# sed "s/samplePath/fbSarGroup/g" output.slurm -i 
# sed 's/sampleDDQNText/fbSarGroup/g' output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm

# sed 's/runDDQN/runSarsaAdditional/g' exp_physical_ddqn.slurm > output.slurm
# sed "s/samplePath/fbSarSuper/g" output.slurm -i 
# sed 's/sampleDDQNText/fbSarSuper/g' output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm