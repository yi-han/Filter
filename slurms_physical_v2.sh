sed 's/sample_sarsa_name/ddTile36/g' exp_physical.slurm > temp1.slurm
sed 's/runSARSA/runSarsaOriginal/g' temp1.slurm > temp2.slurm

sed 's/0 5/0 2/g' temp2.slurm > output.slurm
sbatch output.slurm
sleep 5
sed 's/0 5/2 2/g' temp2.slurm > output.slurm
sbatch output.slurm
sed 's/0 5/4 2/g' temp2.slurm > output.slurm
sbatch output.slurm
sed 's/0 5/6 2/g' temp2.slurm > output.slurm
sbatch output.slurm
sed 's/0 5/8 2/g' temp2.slurm > output.slurm
sbatch output.slurm
sed 's/0 5/10 2/g' temp2.slurm > output.slurm
sbatch output.slurm
sed 's/0 5/12 2/g' temp2.slurm > output.slurm
sbatch output.slurm
sed 's/0 5/14 2/g' temp2.slurm > output.slurm
sbatch output.slurm
sed 's/0 5/16 2/g' temp2.slurm > output.slurm
sbatch output.slurm
sed 's/0 5/18 2/g' temp2.slurm > output.slurm
sbatch output.slurm