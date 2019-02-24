sed 's/runDDQN/runDDQN/g' exp_gpgpu_single.slurm > output.slurm
sed "s/samplePath/$1/g" output.slurm -i 
sed 's/sampleDDQNText/ddMidSinTest/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm


sed 's/runDDQN/runSARSA/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/$1/g" output.slurm -i 
sed 's/sampleDDQNText/sarMidSinTest/g' output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
