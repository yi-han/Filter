# use this if we ever need to remake the entire base
sed 's/runDDQN/runDDQN/g' exp_gpgpu_single.slurm > output.slurm
sed "s/samplePath/$1/g" output.slurm -i 
sed 's/sampleDDQNText/smallSin/g' output.slurm -i 
sed 's/0 2/0 10/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQN/runDDQNAdditional/g' output.slurm -i
sed 's/smallSin/smallMal/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQNAdditional/runDDQNHundred/g' output.slurm -i
sed 's/smallMal/midSin/g' output.slurm -i
sed 's/0 10/0 5/g' output.slurm -i 
sbatch output.slurm
sed 's/0 5/5 5/g' output.slurm -i 
sbatch output.slurm


sed 's/runDDQNHundred/runDDQNMalialis/g' output.slurm -i
sed 's/midSin/midMal/g' output.slurm -i
sed 's/5 5/0 5/g' output.slurm -i 
sbatch output.slurm
sed 's/0 5/5 5/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQNMalialis/runDDQNNetQuick/g' output.slurm -i
sed 's/midMal/midHier/g' output.slurm -i
sed 's/5 5/0 2/g' output.slurm -i 
sbatch output.slurm
sed 's/0 2/2 2/g' output.slurm -i 
sbatch output.slurm
sed 's/2 2/4 2/g' output.slurm -i 
sbatch output.slurm
sed 's/4 2/6 2/g' output.slurm -i 
sbatch output.slurm
sed 's/6 2/8 2/g' output.slurm -i 
sbatch output.slurm

sed 's/runDDQNNetQuick/runSarsaAdditional/g' output.slurm -i
sed 's/midHier/64Sin/g' output.slurm -i
sed 's/8 2/0 5/g' output.slurm -i 
sbatch output.slurm
sed 's/0 5/5 5/g' output.slurm -i 
sbatch output.slurm

sed 's/runSarsaAdditional/runSarsaDDQNCopy/g' output.slurm -i
sed 's/64Sin/64Hier/g' output.slurm -i
sed 's/5 5/0 2/g' output.slurm -i 
sbatch output.slurm
sed 's/0 2/2 2/g' output.slurm -i 
sbatch output.slurm
sed 's/2 2/4 2/g' output.slurm -i 
sbatch output.slurm
sed 's/4 2/6 2/g' output.slurm -i 
sbatch output.slurm
sed 's/6 2/8 2/g' output.slurm -i 
sbatch output.slurm

sed 's/runSarsaDDQNCopy/runSarsaNoOverdrive/g' output.slurm -i
sed 's/64Hier/64_50/g' output.slurm -i
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

