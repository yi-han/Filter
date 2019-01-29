sed 's/runSARSA/runSARSA/g' exp_physical_ddqn.slurm > temp1.slurm
sed 's/sample_sarsa_name/sarsMedium/g' temp1.slurm -i
sed "s/samplePath/$1/g" temp1.slurm > output.slurm
sed 's/0 5/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/runSARSA/runSarsaDDQNCopy/g' output.slurm -i
sbatch output.slurm
sed 's/runSarsaDDQNCopy/runSarsaNoOverdrive/g' output.slurm -i
sbatch output.slurm
# sed 's/runSarsaNoOverdrive/runSarsaOriginal/g' output.slurm -i
# sbatch output.slurm
sed 's/runSarsaNoOverdrive/runSarsaAdditional/g' output.slurm -i
sbatch output.slurm
