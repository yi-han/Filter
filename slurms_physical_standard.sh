sed 's/runSARSA/runSarsaX/g' exp_physical.slurm > output.slurm
sed 's/sample_sarsa_name/advAim64/g' output.slurm -i
sed "s/samplePath/$1/g" output.slurm -i
sed 's/0 5/0 1/g' output.slurm -i
sbatch output.slurm
# sed 's/sample_sarsa_name/sarsa_medium/g' temp1.slurm -i
# sed 's/runSARSA/runSarsaAdditional/g' output.slurm -i
# sbatch output.slurm
# sed 's/runSarsaOriginal/runSarsaNoOverdrive/g' output.slurm -i
# sbatch output.slurm


# sleep 5
# sed 's/0 2/2 2/g' output.slurm -i
# sbatch output.slurm
# sed 's/2 2/4 5/g' output.slurm -i
# sbatch output.slurm
# sed 's/4 5/9 6/g' output.slurm -i
# sbatch output.slurm
# sed 's/9 6/15 5/g' output.slurm -i
# sbatch output.slurm