sed 's/runDDQN/runDDQN/g' exp_gpgpu_single.slurm > temp1.slurm
sed "s/samplePath/$1/g" temp1.slurm -i
sed 's/sampleDDQNText/longCX/g' temp1.slurm > output.slurm
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/runDDQN/runDDQNHundred/g' output.slurm -i
sbatch output.slurm
sed 's/runDDQNHundred/runDDQNMalialis/g' output.slurm -i
sbatch output.slurm
# sed 's/runDDQNMalialis/runDDQNNetQuick/g' output.slurm -i
# sbatch output.slurm
# sed 's/runDDQNNetQuick/runDDQNAdditional/g' output.slurm -i
# sbatch output.slurm
# sed 's/runDDQNAdditional/runSARSA/g' output.slurm -i
# sbatch output.slurm

