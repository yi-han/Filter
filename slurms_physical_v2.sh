# redo base

sed 's/runDDQN/runSARSA/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarConOrig/g' output.slurm -i
sed "s/samplePath/sarConOrig/g" output.slurm -i 
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

sed 's/runDDQN/runSarsaAdditional/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarConSinDD/g' output.slurm -i
sed "s/samplePath/sarConSinDD/g" output.slurm -i 
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


sed 's/runDDQN/runSarsaDDQNCopy/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarConHier/g' output.slurm -i
sed "s/samplePath/sarConHier/g" output.slurm -i 
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


sed 's/runDDQN/runDDQN/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/ddConSin/g' output.slurm -i
sed "s/samplePath/ddConSin/g" output.slurm -i 
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






sed 's/runDDQN/runDDQNAdditional/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/ddConHier/g' output.slurm -i
sed "s/samplePath/ddConHier/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i
sbatch output.slurm
sed 's/3 1/4 1/g' output.slurm -i
sbatch output.slurm
sed 's/4 1/5 1/g' output.slurm -i
sbatch output.slurm
sed 's/5 1/6 1/g' output.slurm -i
sbatch output.slurm
sed 's/6 1/7 1/g' output.slurm -i
sbatch output.slurm
sed 's/7 1/8 1/g' output.slurm -i
sbatch output.slurm
sed 's/8 1/9 1/g' output.slurm -i
sbatch output.slurm


