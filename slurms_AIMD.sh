sed 's/runSARSA/grid_test/g' exp_physical.slurm > output.slurm
sed "s/samplePath/$1/g" output.slurm -i
sed 's/sample_sarsa_name/aimdSmall/g' output.slurm -i
sed 's/0 5//g' output.slurm -i 
# sbatch output.slurm

sed 's/runSARSA/runSarsaAdditional/g' exp_physical.slurm > output.slurm
sed 's/sample_sarsa_name/aimdMid/g' output.slurm -i
sed "s/samplePath/$1/g" output.slurm -i

sbatch output.slurm

sed 's/runSARSA/runSarsaNoOverdrive/g' exp_physical.slurm > output.slurm
sed 's/sample_sarsa_name/aimd64/g' output.slurm -i
sed "s/samplePath/$1/g" output.slurm -i

sbatch output.slurm


