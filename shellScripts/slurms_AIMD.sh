sed 's/runDDQN/grid_test/g' exp_physical.slurm > output.slurm
sed "s/samplePath/$1/g" output.slurm -i
sed 's/sampleDDQNText/aimdSmall/g' output.slurm -i
sed 's/0 5//g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runDDQNAdditional/g' exp_physical.slurm > output.slurm
sed 's/sampleDDQNText/aimdMid/g' output.slurm -i
sed "s/samplePath/$1/g" output.slurm -i
sed 's/0 5//g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runDDQNHundred/g' exp_physical.slurm > output.slurm
sed 's/sampleDDQNText/aimd64/g' output.slurm -i
sed "s/samplePath/$1/g" output.slurm -i
sed 's/0 5//g' output.slurm -i 
sbatch output.slurm


