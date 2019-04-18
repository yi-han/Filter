# mucking exp 2

sed 's/runDDQN/runSARSA/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/ddOver_sarOrig/g' output.slurm -i 
sed "s/samplePath/ddOver_sarOrig/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/2 1/g' output.slurm -i
sbatch output.slurm
sed 's/2 1/4 1/g' output.slurm -i
sbatch output.slurm


sed 's/runDDQN/runSarsaAdditional/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/ddOver_sarSinDD/g' output.slurm -i 
sed "s/samplePath/ddOver_sarSinDD/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/2 1/g' output.slurm -i
sbatch output.slurm
sed 's/2 1/4 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runSarsaDDQNCopy/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/ddOver_sliding/g' output.slurm -i 
sed "s/samplePath/ddOver_sliding/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/2 1/g' output.slurm -i
sbatch output.slurm
sed 's/2 1/4 1/g' output.slurm -i
sbatch output.slurm

# sed 's/runDDQN/runSarsaNoOverdrive/g' exp_cloud.slurm > output.slurm
# sed 's/sampleDDQNText/ddOver_AIMD/g' output.slurm -i 
# sed "s/samplePath/ddOver_AIMD/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 2/2 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/2 1/4 1/g' output.slurm -i
# sbatch output.slurm

# sed 's/runDDQN/runSarsaNoOverdrive/g' exp_cloud.slurm > output.slurm
# sed 's/sampleDDQNText/ddOver_sarHier/g' output.slurm -i 
# sed "s/samplePath/ddOver_sarHier/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 2/2 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/2 1/4 1/g' output.slurm -i
# sbatch output.slurm



# sed 's/runDDQN/runDDQN/g' exp_cloud.slurm > output.slurm
# sed 's/sampleDDQNText/ddOver_ddSin/g' output.slurm -i 
# sed "s/samplePath/ddOver_ddSin/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 1/2 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/2 1/4 1/g' output.slurm -i
# sbatch output.slurm

# sed 's/runDDQN/runDDQNAdditional/g' exp_cloud.slurm > output.slurm
# sed 's/sampleDDQNText/ddOver_ddHier/g' output.slurm -i 
# sed "s/samplePath/ddOver_ddHier/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 1/2 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/2 1/6 1/g' output.slurm -i
# sbatch output.slurm


