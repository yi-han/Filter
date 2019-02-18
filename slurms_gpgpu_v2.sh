sed 's/runDDQN/runDDQNMalialis/g' exp_physical_ddqn.slurm > output.slurm
sed "s/samplePath/$1/g" output.slurm -i
sed 's/sampleDDQNText/mid50/g' output.slurm -i
sed 's/sampleJob/7494582/g' output.slurm -i
sed 's/0 2/0 10/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQNMalialis/runSarsaNoOverdrive/g' output.slurm -i
sed 's/mid50/64_50/g' output.slurm -i
sed 's/7494582/7494583/g' output.slurm -i
sbatch output.slurm


sed 's/runSarsaNoOverdrive/runSarsaDDQNCopy/g' output.slurm -i
sed 's/64_50/64_100/g' output.slurm -i
sed 's/7494583/7494584/g' output.slurm -i
sbatch output.slurm

sed 's/runSarsaDDQNCopy/runDDQNNetQuick/g' output.slurm -i
sed 's/64_50/mid_100/g' output.slurm -i
sed 's/7494584/7494585/g' output.slurm -i
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
