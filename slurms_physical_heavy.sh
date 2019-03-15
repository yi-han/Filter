# aimd trials

sed 's/runDDQN/runDDQN/g' exp_gpgpu_single.slurm > output.slurm
sed 's/sampleDDQNText/ddSingleAimd/g' output.slurm -i
sed "s/samplePath/ddSingleAimd/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runDDQNAdditional/g' exp_gpgpu_single.slurm > output.slurm
sed 's/sampleDDQNText/ddDualAimd/g' output.slurm -i
sed "s/samplePath/ddDualAimd/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runSarsaY/g' exp_gpgpu_single.slurm > output.slurm
sed 's/sampleDDQNText/ddSinEverythingAimd/g' output.slurm -i
sed "s/samplePath/ddSinEverythingAimd/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runDDQNHundred/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarSingleAimd/g' output.slurm -i
sed "s/samplePath/sarSingleAimd/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runDDQNMalialis/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarDualAimd/g' output.slurm -i
sed "s/samplePath/sarDualAimd/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i
sbatch output.slurm