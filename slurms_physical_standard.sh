sed 's/runSARSA/runSARSA/g' exp_physical.slurm > output.slurm
sed 's/sample_sarsa_name/LsMed/g' output.slurm -i
sed "s/samplePath/$1/g" output.slurm -i
sbatch output.slurm
sed 's/0 5/5 5/g' output.slurm -i
sbatch output.slurm


sed 's/LsMed/lS64/g' output.slurm -i
sed 's/runSARSA/runSarsaAdditional/g' output.slurm -i
sed 's/5 5/0 5/g' output.slurm -i
sbatch output.slurm
sed 's/0 5/5 5/g' output.slurm -i
sbatch output.slurm

