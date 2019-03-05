# testing differnt sarsa advesary

sed 's/runDDQN/runSARSA/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/ddEverything/g" output.slurm -i 
sed 's/sampleDDQNText/ddEverything/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm



# sed 's/runDDQN/runSarsaAdditional/g' exp_physical_ddqn.slurm > output.slurm
# sed "s/samplePath/sarGroupLong/g" output.slurm -i 
# sed 's/sampleDDQNText/sarGroupLong/g' output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm

# sed 's/runDDQN/runSarsaDDQNCopy/g' exp_physical_ddqn.slurm > output.slurm
# sed "s/samplePath/sarSplitStandard/g" output.slurm -i 
# sed 's/sampleDDQNText/sarSplitStandard/g' output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm

# sed 's/runDDQN/runSarsaNoOverdrive/g' exp_physical_ddqn.slurm > output.slurm
# sed "s/samplePath/sarSplitLong/g" output.slurm -i 
# sed 's/sampleDDQNText/sarSplitLong/g' output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm

# sed 's/runDDQN/runSarsaOriginal/g' exp_physical_ddqn.slurm > output.slurm
# sed "s/samplePath/sarSuperStandard/g" output.slurm -i 
# sed 's/sampleDDQNText/sarSuperStandard/g' output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm

# sed 's/runDDQN/runSarsaX/g' exp_physical_ddqn.slurm > output.slurm
# sed "s/samplePath/sarSuperLong/g" output.slurm -i 
# sed 's/sampleDDQNText/sarSuperLong/g' output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm

# sed 's/runDDQN/runDDQNAdditional/g' exp_physical_ddqn.slurm > output.slurm
# sed "s/samplePath/sarGroupLowDiscount/g" output.slurm -i 
# sed 's/sampleDDQNText/sarGroupLowDiscount/g' output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm

# sed 's/runDDQN/runDDQNHundred/g' exp_physical_ddqn.slurm > output.slurm
# sed "s/samplePath/sarGroupMidDiscount/g" output.slurm -i 
# sed 's/sampleDDQNText/sarGroupMidDiscount/g' output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm

# sed 's/runDDQN/runDDQNMalialis/g' exp_physical_ddqn.slurm > output.slurm
# sed "s/samplePath/sarGroupAdvAcMany/g" output.slurm -i 
# sed 's/sampleDDQNText/sarGroupAdvAcMany/g' output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm

# sed 's/runDDQN/runDDQNNetQuick/g' exp_physical_ddqn.slurm > output.slurm
# sed "s/samplePath/sarSuperAdvAcMany/g" output.slurm -i 
# sed 's/sampleDDQNText/sarSuperAdvAcMany/g' output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm


