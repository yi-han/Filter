# this is for making all the adv base DDQN + Sarsa


# cp -R LinSarDDQNCopySmall ddGroupSmall
# sed 's/runDDQN/runSARSA/g' exp_gpgpu_single.slurm > output.slurm
# sed "s/samplePath/ddGroupSmall/g" output.slurm -i 
# sed 's/sampleDDQNText/ddGroupSmall/g' output.slurm -i 
# sed 's/0 2/0 2/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 2/2 2/g' output.slurm -i 
# sbatch output.slurm


# cp -R LinSarDDQNCopySmall ddSplitSmall
# sed 's/runDDQN/runSarsaAdditional/g' exp_gpgpu_single.slurm > output.slurm
# sed "s/samplePath/ddSplitSmall/g" output.slurm -i 
# sed 's/sampleDDQNText/ddSplitSmall/g' output.slurm -i 
# sed 's/0 2/0 2/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 2/2 2/g' output.slurm -i 
# sbatch output.slurm

# cp -R LinSarDDQNCopySmall sarGroupSmall
# sed 's/runDDQN/runSarsaDDQNCopy/g' exp_physical_ddqn.slurm > output.slurm
# sed "s/samplePath/sarGroupSmall/g" output.slurm -i 
# sed 's/sampleDDQNText/sarGroupSmall/g' output.slurm -i 
# sed 's/0 2/0 2/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 2/2 2/g' output.slurm -i 
# sbatch output.slurm

# cp -R LinSarDDQNCopySmall sarSplitSmall
# sed 's/runDDQN/runSarsaNoOverdrive/g' exp_physical_ddqn.slurm > output.slurm
# sed "s/samplePath/sarSplitSmall/g" output.slurm -i 
# sed 's/sampleDDQNText/sarSplitSmall/g' output.slurm -i 
# sed 's/0 2/0 2/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 2/2 2/g' output.slurm -i 
# sbatch output.slurm

cp -R LinSarDDQNCopyMid ddGroupMid
sed 's/runDDQN/runSarsaOriginal/g' exp_gpgpu_single.slurm > output.slurm
sed "s/samplePath/ddGroupMid/g" output.slurm -i 
sed 's/sampleDDQNText/ddGroupMid/g' output.slurm -i 
sed 's/0 2/0 2/g' output.slurm -i 
sbatch output.slurm
sed 's/0 2/2 2/g' output.slurm -i 
sbatch output.slurm

cp -R LinSarDDQNCopyMid ddSplitMid
sed 's/runDDQN/runSarsaX/g' exp_gpgpu_single.slurm > output.slurm
sed "s/samplePath/ddSplitMid/g" output.slurm -i 
sed 's/sampleDDQNText/ddSplitMid/g' output.slurm -i 
sed 's/0 2/0 2/g' output.slurm -i 
sbatch output.slurm
sed 's/0 2/2 2/g' output.slurm -i 
sbatch output.slurm

cp -R LinSarDDQNCopyMid sarGroupMid
sed 's/runDDQN/runSarsaY/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/sarGroupMid/g" output.slurm -i 
sed 's/sampleDDQNText/sarGroupMid/g' output.slurm -i 
sed 's/0 2/0 2/g' output.slurm -i 
sbatch output.slurm
sed 's/0 2/2 2/g' output.slurm -i 
sbatch output.slurm

cp -R LinSarDDQNCopyMid sarSplitMid
sed 's/runDDQN/runSarsaZ/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/sarSplitMid/g" output.slurm -i 
sed 's/sampleDDQNText/sarSplitMid/g' output.slurm -i 
sed 's/0 2/0 2/g' output.slurm -i 
sbatch output.slurm
sed 's/0 2/2 2/g' output.slurm -i 
sbatch output.slurm

cp -R LinSarDDQNCopy64 ddGroup64
sed 's/runDDQN/runDDQNAdditional/g' exp_gpgpu_single.slurm > output.slurm
sed "s/samplePath/ddGroup64/g" output.slurm -i 
sed 's/sampleDDQNText/ddGroup64/g' output.slurm -i 
sed 's/0 2/0 2/g' output.slurm -i 
sbatch output.slurm
sed 's/0 2/2 2/g' output.slurm -i 
sbatch output.slurm

cp -R LinSarDDQNCopy64 ddSplit64
sed 's/runDDQN/runDDQNHundred/g' exp_gpgpu_single.slurm > output.slurm
sed "s/samplePath/ddSplit64/g" output.slurm -i 
sed 's/sampleDDQNText/ddSplit64/g' output.slurm -i 
sed 's/0 2/0 2/g' output.slurm -i 
sbatch output.slurm
sed 's/0 2/2 2/g' output.slurm -i 
sbatch output.slurm

cp -R LinSarDDQNCopy64 sarGroup64
sed 's/runDDQN/runDDQNMalialis/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/sarGroup64/g" output.slurm -i 
sed 's/sampleDDQNText/sarGroup64/g' output.slurm -i 
sed 's/0 2/0 2/g' output.slurm -i 
sbatch output.slurm
sed 's/0 2/2 2/g' output.slurm -i 
sbatch output.slurm

cp -R LinSarDDQNCopy64 sarSplit64
sed 's/runDDQN/runDDQNNetQuick/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/sarSplit64/g" output.slurm -i 
sed 's/sampleDDQNText/sarSplit64/g' output.slurm -i 
sed 's/0 2/0 2/g' output.slurm -i 
sbatch output.slurm
sed 's/0 2/2 2/g' output.slurm -i 
sbatch output.slurm


