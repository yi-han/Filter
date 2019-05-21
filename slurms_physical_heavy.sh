# aimd testing

sed 's/runDDQN/runAimdJeremy/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/ddAimd/g' output.slurm -i
sed "s/samplePath/ddAimd/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runSarsaAdditional/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/ddAimdSingle/g' output.slurm -i
sed "s/samplePath/ddAimdSingle/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runSarsaDDQNCopy/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/ddAimdRoles/g' output.slurm -i
sed "s/samplePath/ddAimdRoles/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runSarsaNoOverdrive/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/ddAimdRolesSingle/g' output.slurm -i
sed "s/samplePath/ddAimdRolesSingle/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runSarsaOriginal/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/ddAimdLoads/g' output.slurm -i
sed "s/samplePath/ddAimdLoads/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runSarsaX/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/ddAimdLoadsSingle/g' output.slurm -i
sed "s/samplePath/ddAimdLoadsSingle/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm


sed 's/runDDQN/runSarsaY/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/ddAimdBoth/g' output.slurm -i
sed "s/samplePath/ddAimdBoth/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm


sed 's/runDDQN/runSarsaZ/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/ddAimdBothSingle/g' output.slurm -i
sed "s/samplePath/ddAimdBothSingle/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm


