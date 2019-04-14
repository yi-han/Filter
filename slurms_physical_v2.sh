# base for exp1

sed 's/runDDQN/runSARSA/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarOrig/g' output.slurm -i
sed "s/samplePath/sarOrig/g" output.slurm -i 
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
sed 's/sampleDDQNText/sarSinDD/g' output.slurm -i
sed "s/samplePath/sarSinDD/g" output.slurm -i 
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
sed 's/sampleDDQNText/sarHier/g' output.slurm -i
sed "s/samplePath/sarHier/g" output.slurm -i 
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

# sed 's/runDDQN/runSarsaNoOverdrive/g' exp_cloud.slurm > output.slurm
# sed 's/sampleDDQNText/sarHier/g' output.slurm -i
# sed "s/samplePath/sarHier/g" output.slurm -i 
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

# sed 's/runDDQN/runSarsaOriginal/g' exp_cloud.slurm > output.slurm
# sed 's/sampleDDQNText/sarHierMem/g' output.slurm -i
# sed "s/samplePath/sarHierMem/g" output.slurm -i 
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


sed 's/runDDQN/runDDQN/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/ddSin/g' output.slurm -i
sed "s/samplePath/ddSin/g" output.slurm -i 
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
sed 's/sampleDDQNText/ddHier/g' output.slurm -i
sed "s/samplePath/ddHier/g" output.slurm -i 
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


# sed 's/runDDQN/runDDQNHundred/g' exp_cloud.slurm > output.slurm
# sed 's/sampleDDQNText/ddHier/g' output.slurm -i
# sed "s/samplePath/ddHier/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/2 1/3 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/3 1/4 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/4 1/5 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/5 1/6 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/6 1/7 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/7 1/8 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/8 1/9 1/g' output.slurm -i
# sbatch output.slurm

# sed 's/runDDQN/runDDQNMalialis/g' exp_cloud.slurm > output.slurm
# sed 's/sampleDDQNText/ddHierMem/g' output.slurm -i
# sed "s/samplePath/ddHierMem/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/2 1/3 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/3 1/4 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/4 1/5 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/5 1/6 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/6 1/7 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/7 1/8 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/8 1/9 1/g' output.slurm -i
# sbatch output.slurm


