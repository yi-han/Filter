sed 's/runSARSA/runSARSA/g' exp_physical.slurm > temp1.slurm
sed 's/sample_sarsa_name/drift25/g' temp1.slurm -i
sed "s/samplePath/$1/g" temp1.slurm > output.slurm
sed 's/0 5/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/runSARSA/runSarsaDDQNCopy/g' temp1.slurm -i
sbatch output.slurm
sed 's/runSarsaDDQNCopy/runSarsaNoOverdrive/g' temp1.slurm -i
sbatch output.slurm
sed 's/runSarsaNoOverdrive/runSarsaOriginal/g' temp1.slurm -i
sbatch output.slurm
sed 's/runSarsaOriginal/runSarsaAdditional.py/g' temp1.slurm -i
sbatch output.slurm
