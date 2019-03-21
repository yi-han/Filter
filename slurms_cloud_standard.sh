# standard tests

sed 's/runDDQN/runSARSA/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarConOrig/g' output.slurm -i
sed "s/samplePath/sarConOrig/g" output.slurm -i 
sed 's/0 2/0 10/g' output.slurm -i
sbatch output.slurm


sed 's/runDDQN/runSarsaAdditional/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarConSinDD/g' output.slurm -i
sed "s/samplePath/sarConSinDD/g" output.slurm -i 
sed 's/0 2/0 10/g' output.slurm -i
sbatch output.slurm



sed 's/runDDQN/runSarsaDDQNCopy/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarConHier/g' output.slurm -i
sed "s/samplePath/sarConHier/g" output.slurm -i 
sed 's/0 2/0 10/g' output.slurm -i
sbatch output.slurm



sed 's/runDDQN/runDDQN/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/ddConSin/g' output.slurm -i
sed "s/samplePath/ddConSin/g" output.slurm -i 
sed 's/0 2/0 10/g' output.slurm -i
sbatch output.slurm




sed 's/runDDQN/runDDQNAdditional/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/ddConHier/g' output.slurm -i
sed "s/samplePath/ddConHier/g" output.slurm -i 
sed 's/0 2/0 10/g' output.slurm -i
sbatch output.slurm


