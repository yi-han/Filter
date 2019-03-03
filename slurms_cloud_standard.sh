# 
sed 's/runDDQN/runSARSA/g' exp_gpgpu_single.slurm > output.slurm
sed "s/samplePath/ddEverything/g" output.slurm -i 
sed 's/sampleDDQNText/ddEverything/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

# sed 's/runDDQN/runDDQNAdditional/g' exp_gpgpu_single.slurm > output.slurm
# sed "s/samplePath/ddAimdVariant/g" output.slurm -i 
# sed 's/sampleDDQNText/ddAimdVariant/g' output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm

# sed 's/runDDQN/runSARSA/g' exp_physical_ddqn.slurm > output.slurm
# sed "s/samplePath/ssAimdNormal/g" output.slurm -i 
# sed 's/sampleDDQNText/ssAimdNormal/g' output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm


# sed 's/runDDQN/runSarsaAdditional/g' exp_physical_ddqn.slurm > output.slurm
# sed "s/samplePath/ssAimdVariant/g" output.slurm -i 
# sed 's/sampleDDQNText/ssAimdVariant/g' output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm

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