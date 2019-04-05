# malialis small exp 1. 

sed 's/runDDQN/runDDQN/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/ddConSin/g' output.slurm -i
sed "s/samplePath/ddSin/g" output.slurm -i 
sed 's/0 2/0 2/g' output.slurm -i
sbatch output.slurm
sed 's/0 2/2 2/g' output.slurm -i
sbatch output.slurm
sed 's/0 2/4 2/g' output.slurm -i
sbatch output.slurm
sed 's/0 2/6 2/g' output.slurm -i
sbatch output.slurm
sed 's/0 2/8 2/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runSARSA/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarOriginal/g' output.slurm -i
sed "s/samplePath/sarOriginal/g" output.slurm -i 
sed 's/0 2/0 2/g' output.slurm -i
sbatch output.slurm
sed 's/0 2/2 2/g' output.slurm -i
sbatch output.slurm
sed 's/0 2/4 2/g' output.slurm -i
sbatch output.slurm
sed 's/0 2/6 2/g' output.slurm -i
sbatch output.slurm
sed 's/0 2/8 2/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runSarsaAdditional/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarSin100/g' output.slurm -i
sed "s/samplePath/sarSin100/g" output.slurm -i 
sed 's/0 2/0 2/g' output.slurm -i
sbatch output.slurm
sed 's/0 2/2 2/g' output.slurm -i
sbatch output.slurm
sed 's/0 2/4 2/g' output.slurm -i
sbatch output.slurm
sed 's/0 2/6 2/g' output.slurm -i
sbatch output.slurm
sed 's/0 2/8 2/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runSarsaDDQNCopy/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/AIMD/g' output.slurm -i
sed "s/samplePath/AIMD/g" output.slurm -i 
sed 's/0 2/0 2/g' output.slurm -i
sbatch output.slurm
sed 's/0 2/2 2/g' output.slurm -i
sbatch output.slurm
sed 's/0 2/4 2/g' output.slurm -i
sbatch output.slurm
sed 's/0 2/6 2/g' output.slurm -i
sbatch output.slurm
sed 's/0 2/8 2/g' output.slurm -i
sbatch output.slurm