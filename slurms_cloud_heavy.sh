sed 's/runDDQN/runDDQN/g' exp_gpgpu_single.slurm > output.slurm
sed "s/samplePath/ddMidAimdNormal/g" output.slurm -i 
sed 's/sampleDDQNText/ddMidAimdNormal/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm


sed 's/runDDQN/runDDQNAdditional/g' exp_gpgpu_single.slurm > output.slurm
sed "s/samplePath/ddMidAimdVariant/g" output.slurm -i 
sed 's/sampleDDQNText/ddMidAimdVariant/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runDDQNHundred/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/sarMidAimdNormal/g" output.slurm -i 
sed 's/sampleDDQNText/sarMidAimdNormal/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runDDQNMalialis/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/sarMidAimdVariant/g" output.slurm -i 
sed 's/sampleDDQNText/sarMidAimdVariant/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm