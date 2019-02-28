# 
sed 's/runDDQN/runDDQN/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/ddAdvVariant/g" output.slurm -i 
sed 's/sampleDDQNText/ddAdvVariant/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runDDQNAdditional/g' exp_gpgpu_single.slurm > output.slurm
sed "s/samplePath/sarAdvVariant/g" output.slurm -i 
sed 's/sampleDDQNText/sarAdvVariant/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

# sed 's/runDDQN/runDDQNHundred/g' exp_gpgpu_single.slurm > output.slurm
# sed "s/samplePath/dMidSuperHigh/g" output.slurm -i 
# sed 's/sampleDDQNText/dMidGroupHigh/g' output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm

# sed 's/runDDQN/runDDQNMalialis/g' exp_gpgpu_single.slurm > output.slurm
# sed "s/samplePath/dMidSuperLow/g" output.slurm -i 
# sed 's/sampleDDQNText/dMidSuperLow/g' output.slurm -i 
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