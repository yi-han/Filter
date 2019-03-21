# aimd tests

sed 's/runDDQN/runDDQN/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/ddSingleAimd/g' output.slurm -i
sed "s/samplePath/ddSingleAimd/g" output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runDDQNAdditional/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/ddDualAimd/g' output.slurm -i
sed "s/samplePath/ddDualAimd/g" output.slurm -i 
sbatch output.slurm


sed 's/runDDQN/runSarsaY/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/ddSinEverythingAimd/g' output.slurm -i
sed "s/samplePath/ddSinEverythingAimd/g" output.slurm -i 
sbatch output.slurm


sed 's/runDDQN/runDDQNHundred/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarSingleAimd/g' output.slurm -i
sed "s/samplePath/sarSingleAimd/g" output.slurm -i 
sed 's/0 2/0 4/g' output.slurm -i
sbatch output.slurm


sed 's/runDDQN/runDDQNMalialis/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarDualAimd/g' output.slurm -i
sed "s/samplePath/sarDualAimd/g" output.slurm -i 
sed 's/0 2/0 4/g' output.slurm -i
sbatch output.slurm