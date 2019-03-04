# doing all the tests
sed 's/runDDQN/runDDQN/g' exp_physical.slurm > output.slurm
sed "s/samplePath/$1/g" output.slurm -i 
sed 's/sample_sarsa_name/smallSin/g' output.slurm -i 
sed 's/0 5/0 2/g' output.slurm -i 
sbatch output.slurm
sed 's/0 2/2 2/g' output.slurm -i 
sbatch output.slurm
sed 's/2 2/4 2/g' output.slurm -i 
sbatch output.slurm
sed 's/4 2/6 2/g' output.slurm -i 
sbatch output.slurm
sed 's/6 2/8 2/g' output.slurm -i 
sbatch output.slurm


sed 's/runDDQN/runDDQNAdditional/g' output.slurm -i
sed 's/smallSin/smallMal/g' output.slurm -i
sed 's/8 2/0 2/g' output.slurm -i 
sbatch output.slurm
sed 's/0 2/2 2/g' output.slurm -i 
sbatch output.slurm
sed 's/2 2/4 2/g' output.slurm -i 
sbatch output.slurm
sed 's/4 2/6 2/g' output.slurm -i 
sbatch output.slurm
sed 's/6 2/8 2/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQNAdditional/runDDQNHundred/g' output.slurm -i
sed 's/smallMal/midSin/g' output.slurm -i
sed 's/8 2/0 2/g' output.slurm -i 
sbatch output.slurm
sed 's/0 2/2 2/g' output.slurm -i 
sbatch output.slurm
sed 's/2 2/4 2/g' output.slurm -i 
sbatch output.slurm
sed 's/4 2/6 2/g' output.slurm -i 
sbatch output.slurm
sed 's/6 2/8 2/g' output.slurm -i 
sbatch output.slurm


sed 's/runDDQNHundred/runDDQNMalialis/g' output.slurm -i
sed 's/midSin/mid50/g' output.slurm -i
sed 's/8 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/2 1/g' output.slurm -i 
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i 
sbatch output.slurm
sed 's/3 1/4 1/g' output.slurm -i 
sbatch output.slurm
sed 's/4 1/5 1/g' output.slurm -i 
sbatch output.slurm
sed 's/5 1/6 1/g' output.slurm -i 
sbatch output.slurm
sed 's/6 1/7 1/g' output.slurm -i 
sbatch output.slurm
sed 's/7 1/8 1/g' output.slurm -i 
sbatch output.slurm
sed 's/8 1/9 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQNMalialis/runDDQNNetQuick/g' output.slurm -i
sed 's/mid50/midHier/g' output.slurm -i
sed 's/9 1/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/2 1/g' output.slurm -i 
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i 
sbatch output.slurm
sed 's/3 1/4 1/g' output.slurm -i 
sbatch output.slurm
sed 's/4 1/5 1/g' output.slurm -i 
sbatch output.slurm
sed 's/5 1/6 1/g' output.slurm -i 
sbatch output.slurm
sed 's/6 1/7 1/g' output.slurm -i 
sbatch output.slurm
sed 's/7 1/8 1/g' output.slurm -i 
sbatch output.slurm
sed 's/8 1/9 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQNNetQuick/runSarsaAdditional/g' output.slurm -i
sed 's/midHier/64Sin/g' output.slurm -i
sed 's/9 1/0 2/g' output.slurm -i 
sbatch output.slurm
sed 's/0 2/2 2/g' output.slurm -i 
sbatch output.slurm
sed 's/2 2/4 2/g' output.slurm -i 
sbatch output.slurm
sed 's/4 2/6 2/g' output.slurm -i 
sbatch output.slurm
sed 's/6 2/8 2/g' output.slurm -i 
sbatch output.slurm


sed 's/runSarsaAdditional/runSarsaDDQNCopy/g' output.slurm -i
sed 's/64Sin/64Hier/g' output.slurm -i
sed 's/8 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/2 1/g' output.slurm -i 
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i 
sbatch output.slurm
sed 's/3 1/4 1/g' output.slurm -i 
sbatch output.slurm
sed 's/4 1/5 1/g' output.slurm -i 
sbatch output.slurm
sed 's/5 1/6 1/g' output.slurm -i 
sbatch output.slurm
sed 's/6 1/7 1/g' output.slurm -i 
sbatch output.slurm
sed 's/7 1/8 1/g' output.slurm -i 
sbatch output.slurm
sed 's/8 1/9 1/g' output.slurm -i 
sbatch output.slurm

sed 's/runSarsaDDQNCopy/runSarsaNoOverdrive/g' output.slurm -i
sed 's/64Hier/64_50/g' output.slurm -i
sed 's/9 1/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/2 1/g' output.slurm -i 
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i 
sbatch output.slurm
sed 's/3 1/4 1/g' output.slurm -i 
sbatch output.slurm
sed 's/4 1/5 1/g' output.slurm -i 
sbatch output.slurm
sed 's/5 1/6 1/g' output.slurm -i 
sbatch output.slurm
sed 's/6 1/7 1/g' output.slurm -i 
sbatch output.slurm
sed 's/7 1/8 1/g' output.slurm -i 
sbatch output.slurm
sed 's/8 1/9 1/g' output.slurm -i 
sbatch output.slurm
