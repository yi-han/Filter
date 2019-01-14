sed 's/runSARSA/runSARSA/g' exp_physical.slurm > temp1.slurm
sed 's/sample_sarsa_name/ssixfour/g' temp1.slurm -i
sed "s/samplePath/$1/g" temp1.slurm > output.slurm

sed 's/0 5/0 1/g' output.slurm -i
sbatch output.slurm
# sleep 5
# sed 's/0 5/2 2/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 5/4 2/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 5/6 2/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 5/8 2/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 5/10 2/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 5/12 2/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 5/14 2/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 5/16 2/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 5/18 2/g' output.slurm -i
# sbatch output.slurm