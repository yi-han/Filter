sed 's/runDDQN/runDDQN/g' exp_gpgpu_single.slurm > output.slurm
sed "s/samplePath/$1/g" output.slurm -i
sed 's/sampleDDQNText/advSmall/g' output.slurm -i
# sbatch output.slurm
# sleep 5
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runDDQNAdditional/g' output.slurm -i
sed 's/advSmall/advMid/g' output.slurm -i
sed 's/1 1/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQNAdditional/runDDQNHundred/g' output.slurm -i
sed 's/advMid/advSixFour/g' output.slurm -i
sed 's/1 1/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm


