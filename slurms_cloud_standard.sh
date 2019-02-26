# 
sed 's/runDDQN/runDDQN/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/sAdvAimdSmall/g" output.slurm -i 
sed 's/sampleDDQNText/sAdvAimdSmall/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runDDQNAdditional/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/sAdvAimdSMid/g" output.slurm -i 
sed 's/sampleDDQNText/sAdvAimdSMid/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

# sed 's/runDDQN/runDDQNHundred/g' exp_physical_ddqn.slurm > output.slurm
# sed "s/samplePath/$1/g" output.slurm -i 
# sed 's/sampleDDQNText/sAdvAimdSmall/g' output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# # sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm

# sed 's/runDDQN/runDDQNMalialis/g' exp_gpgpu_single.slurm > output.slurm
# sed "s/samplePath/sTeamDd100SingAdvDdqnSuperLow/g" output.slurm -i 
# sed 's/sampleDDQNText/fbSarSuper/g' output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# # sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm

# sed 's/runDDQN/runDDQNNetQuick/g' exp_physical_ddqn.slurm > output.slurm
# sed "s/samplePath/sTeamDd100SingAdvSarGroup/g" output.slurm -i 
# sed 's/sampleDDQNText/fbSarSuper/g' output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# # sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm

# sed 's/runDDQN/runSarsaAdditional/g' exp_physical_ddqn.slurm > output.slurm
# sed "s/samplePath/sTeamDd100SingAdvSarSuper/g" output.slurm -i 
# sed 's/sampleDDQNText/fbSarSuper/g' output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# # sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm