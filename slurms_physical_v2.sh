sed 's/runSARSA/grid_test/g' exp_physical.slurm > temp1.slurm
sed 's/sample_sarsa_name/grid_test/g' temp1.slurm -i
sed "s/samplePath/$1/g" temp1.slurm > output.slurm

sed 's/0 5//g' output.slurm -i
sbatch output.slurm
sed 's/grid_test/runSarsaOriginal/g' output.slurm -i
sbatch output.slurm

# sleep 5
# sed 's/0 2/2 2/g' output.slurm -i
# sbatch output.slurm
# sed 's/2 2/4 5/g' output.slurm -i
# sbatch output.slurm
# sed 's/4 5/9 6/g' output.slurm -i
# sbatch output.slurm
# sed 's/9 6/15 5/g' output.slurm -i
# sbatch output.slurm