sed 's/runDDQN/runSARSA/g' exp_gpgpu_single.slurm > output.slurm
sed "s/samplePath/ddMidAimdVariant/g" output.slurm -i 
sed 's/sampleDDQNText/ddMidAimdVariant/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm


sed 's/runDDQN/runSarsaAdditional/g' exp_gpgpu_single.slurm > output.slurm
sed "s/samplePath/ddMidAimdExtended/g" output.slurm -i 
sed 's/sampleDDQNText/ddMidAimdExtended/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runSarsaDDQNCopy/g' exp_cloud.slurm > output.slurm
sed "s/samplePath/sarMidAimdVariant/g" output.slurm -i 
sed 's/sampleDDQNText/sarMidAimdVariant/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runSarsaNoOverdrive/g' exp_cloud.slurm > output.slurm
sed "s/samplePath/sarMidAimdExtended/g" output.slurm -i 
sed 's/sampleDDQNText/sarMidAimdExtended/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm