sed 's/runDDQN/runDDQNNetQuick/g' exp_gpgpu_single.slurm > temp1.slurm
sed 's/sampleDDQNText/DD6Four/g' temp1.slurm > temp2.slurm
sed 's/sampleDDQNText/DD6Four/g' temp1.slurm > output.slurm
sbatch output.slurm
sleep 5
sed 's/0 2/2 2/g' temp2.slurm > output.slurm
sbatch output.slurm
sed 's/0 2/4 2/g' temp2.slurm > output.slurm
sbatch output.slurm
sed 's/0 2/6 2/g' temp2.slurm > output.slurm
sbatch output.slurm
sed 's/0 2/8 2/g' temp2.slurm > output.slurm
sbatch output.slurm
sed 's/0 2/10 2/g' temp2.slurm > output.slurm
sbatch output.slurm
sed 's/0 2/12 2/g' temp2.slurm > output.slurm
sbatch output.slurm
sed 's/0 2/14 2/g' temp2.slurm > output.slurm
sbatch output.slurm
sed 's/0 2/16 2/g' temp2.slurm > output.slurm
sbatch output.slurm
sed 's/0 2/18 2/g' temp2.slurm > output.slurm
sbatch output.slurm
