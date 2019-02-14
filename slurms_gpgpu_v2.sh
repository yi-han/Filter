sed 's/runDDQN/runDDQN/g' exp_gpgpu_single.slurm > output.slurm
sed "s/samplePath/$1/g" output.slurm -i
sed 's/sampleDDQNText/advSAim/g' output.slurm -i
# sbatch output.slurm
# sleep 5
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/runDDQN/runDDQNAdditional/g' output.slurm -i
sed 's/advSAim/advMAim/g' output.slurm -i
sbatch output.slurm
sed 's/runDDQNAdditional/runDDQNHundred/g' output.slurm -i
sed 's/advMAim/adv64Aim/g' output.slurm -i
sbatch output.slurm


# sed 's/runDDQN/runDDQNAdditional/g' output.slurm -i
# sed 's/malSmall/malMedium/g' output.slurm -i
# sbatch output.slurm
# sed 's/runDDQNAdditional/runDDQNHundred/g' output.slurm -i
# sed 's/malMedium/hier/g' output.slurm -i
# sbatch output.slurm

# sed 's/0 2/6 2/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 2/8 2/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 2/10 2/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 2/12 2/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 2/14 2/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 2/16 2/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 2/18 2/g' output.slurm -i
# sbatch output.slurm
