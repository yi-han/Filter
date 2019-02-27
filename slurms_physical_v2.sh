# redo sarsa base

# sed 's/runDDQN/runSARSA/g' exp_physical_ddqn.slurm > output.slurm
# sed 's/sampleDDQNText/sarOriSmall/g' output.slurm -i
# sed "s/samplePath/$1/g" output.slurm -i 
# sed 's/0 2/0 5/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 5/5 5/g' output.slurm -i
# sbatch output.slurm




# sed 's/runDDQN/runSarsaAdditional/g' exp_physical_ddqn.slurm > output.slurm
# sed 's/sampleDDQNText/sar100Small/g' output.slurm -i
# sed "s/samplePath/$1/g" output.slurm -i 
# sed 's/0 2/0 5/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 5/5 5/g' output.slurm -i
# sbatch output.slurm

# sed 's/runDDQN/runSarsaDDQNCopy/g' exp_physical_ddqn.slurm > output.slurm
# sed 's/sampleDDQNText/sarOriMid/g' output.slurm -i
# sed "s/samplePath/$1/g" output.slurm -i 
# sed 's/0 2/0 5/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 5/5 5/g' output.slurm -i
# sbatch output.slurm

# sed 's/runDDQN/runSarsaNoOverdrive/g' exp_physical_ddqn.slurm > output.slurm
# sed 's/sampleDDQNText/sar100mid/g' output.slurm -i
# sed "s/samplePath/$1/g" output.slurm -i 
# sed 's/0 2/0 5/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 5/5 5/g' output.slurm -i
# sbatch output.slurm


# sed 's/runDDQN/runSarsaOriginal/g' exp_physical_ddqn.slurm > output.slurm
# sed 's/sampleDDQNText/sar200mid/g' output.slurm -i
# sed "s/samplePath/$1/g" output.slurm -i 
# sed 's/0 2/0 2/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 2/2 2/g' output.slurm -i 
# sbatch output.slurm
# sed 's/2 2/4 2/g' output.slurm -i 
# sbatch output.slurm
# sed 's/4 2/6 2/g' output.slurm -i 
# sbatch output.slurm
# sed 's/6 2/8 2/g' output.slurm -i 
# sbatch output.slurm

# sed 's/runDDQN/runSarsaX/g' exp_physical_ddqn.slurm > output.slurm
# sed 's/sampleDDQNText/sarOri64/g' output.slurm -i
# sed "s/samplePath/$1/g" output.slurm -i 
# sed 's/0 2/0 5/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 5/5 5/g' output.slurm -i
# sbatch output.slurm

# sed 's/runDDQN/runDDQNAdditional/g' exp_physical_ddqn.slurm > output.slurm
# sed 's/sampleDDQNText/sar10064/g' output.slurm -i
# sed "s/samplePath/$1/g" output.slurm -i 
# sed 's/0 2/0 5/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 5/5 5/g' output.slurm -i
# sbatch output.slurm

sed 's/runDDQN/runDDQNHundred/g' exp_physical_ddqn.slurm > output.slurm
sed 's/sampleDDQNText/sar20064/g' output.slurm -i
sed "s/samplePath/$1/g" output.slurm -i 
sed 's/0 2/0 2/g' output.slurm -i
sbatch output.slurm
sed 's/0 2/2 2/g' output.slurm -i 
sbatch output.slurm
sed 's/2 2/4 2/g' output.slurm -i 
sbatch output.slurm
sed 's/4 2/6 2/g' output.slurm -i 
sbatch output.slurm
sed 's/6 2/8 2/g' output.slurm -i 
sbatch output.slurm
# sbatch output.slurm