# mucking exp 2
sed 's/runDDQN/runSARSA/g' exp_either.slurm > output.slurm
sed 's/sampleDDQNText/ddAdvSarSinNor/g' output.slurm -i
sed "s/samplePath/ddAdvSarSinNor/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runSarsaAdditional/g' exp_either.slurm > output.slurm
sed 's/sampleDDQNText/ddAdvSlidingDdSin/g' output.slurm -i
sed "s/samplePath/ddAdvSlidingDdSin/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm



