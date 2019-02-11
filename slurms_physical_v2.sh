sed 's/runSARSA/runSARSA/g' exp_physical.slurm > output.slurm
sed 's/sample_sarsa_name/LSSsmall/g' output.slurm -i
sed "s/samplePath/$1/g" output.slurm -i 

sed 's/0 5/0 10/g' output.slurm -i
sbatch output.slurm
sed 's/runSARSA/runSarsaOriginal/g' output.slurm -i
sed 's/LSSsmall/L200Med/g' output.slurm -i
sed 's/0 10/0 2/g' output.slurm -i
sbatch output.slurm
sed 's/0 2/2 4/g' output.slurm -i
sbatch output.slurm
sed 's/2 4/6 4/g' output.slurm -i
sbatch output.slurm

sed 's/runSarsaOriginal/runSarsaX/g' output.slurm -i
sed 's/L200Med/L200_64/g' output.slurm -i
sed 's/6 4/0 2/g' output.slurm -i
sbatch output.slurm
sed 's/0 2/2 4/g' output.slurm -i
sbatch output.slurm
sed 's/2 4/6 4/g' output.slurm -i
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