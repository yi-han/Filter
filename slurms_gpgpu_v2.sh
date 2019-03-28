# aimd base

sed 's/runDDQN/runDDQN/g' exp_gpgpu_single.slurm > output.slurm
sed 's/sampleDDQNText/ddAimd/g' output.slurm -i
sed "s/samplePath/ddAimd/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runDDQNAdditional/g' exp_gpgpu_single.slurm > output.slurm
sed 's/sampleDDQNText/ddAimdExtProper/g' output.slurm -i
sed "s/samplePath/ddAimdExtProper/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm


sed 's/runDDQN/runDDQNHundred/g' exp_cloud.slurm > output.slurm
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

