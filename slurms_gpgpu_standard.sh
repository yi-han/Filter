
sed 's/runDDQN/runDDQN/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/ddConSin/g' output.slurm -i
sed "s/samplePath/ddSin/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm




sed 's/runDDQN/runDDQNAdditional/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/ddConHier/g' output.slurm -i
sed "s/samplePath/ddSinMem/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm


sed 's/runDDQN/runDDQNHundred/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/ddConHier/g' output.slurm -i
sed "s/samplePath/ddHier/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm


sed 's/runDDQN/runDDQNMalialis/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/ddConHier/g' output.slurm -i
sed "s/samplePath/ddHierMem/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
