# aimd base

sed 's/runDDQN/runDDQN/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/ddAimd/g' output.slurm -i
sed "s/samplePath/ddAimd/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i
sbatch output.slurm

#sed 's/runDDQN/runDDQNAdditional/g' exp_gpgpu_single.slurm > output.slurm
sed 's/runDDQN/runDDQNAdditional/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/ddAimdAlt1/g' output.slurm -i
sed "s/samplePath/ddAimdAlt1/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i
sbatch output.slurm


sed 's/runDDQN/runDDQNHundred/g' exp_gpgpu_single.slurm > output.slurm
# sed 's/runDDQN/runDDQNHundred/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/ddAimdLarge/g' output.slurm -i
sed "s/samplePath/ddAimdLarge/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runSarsaY/g' exp_gpgpu_single.slurm > output.slurm
sed 's/sampleDDQNText/ddAimdExtreme/g' output.slurm -i
sed "s/samplePath/ddAimdExtreme/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runDDQNMalialis/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarAimd/g' output.slurm -i
sed "s/samplePath/sarAimd/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i
sbatch output.slurm


sed 's/runDDQN/runDDQNNetQuick/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarAimdAlt1/g' output.slurm -i
sed "s/samplePath/sarAimdAlt1/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runSarsaZ/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarAimdLarge/g' output.slurm -i
sed "s/samplePath/sarAimdLarge/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i
sbatch output.slurm


