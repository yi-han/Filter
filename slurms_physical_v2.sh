# all the sarsa ones

sed 's/runDDQN/runSARSA/g' exp_physical_ddqn.slurm > output.slurm
sed 's/sampleDDQNText/LsMid/g' output.slurm -i
sed "s/samplePath/$1/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
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



sed 's/runSARSA/runSarsaAdditional/g' output.slurm -i
sed 's/LsMid/Ls64/g' output.slurm -i
sed 's/9 1/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
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




# sed 's/runSarsaAdditional/runSarsaDDQNCopy/g' output.slurm -i
# sed 's/LDsinSmall/LsMid/g' output.slurm -i
# sed 's/5 5/0 5/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 5/5 5/g' output.slurm -i
# sbatch output.slurm

# sed 's/runSarsaDDQNCopy/runSarsaNoOverdrive/g' output.slurm -i
# sed 's/LsMid/LD200Mid/g' output.slurm -i
# sed 's/5 5/0 2/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 2/2 2/g' output.slurm -i 
# sbatch output.slurm
# sed 's/2 2/4 2/g' output.slurm -i 
# sbatch output.slurm
# sed 's/4 2/6 2/g' output.slurm -i 
# sbatch output.slurm
# sed 's/6 2/8 2/g' output.slurm -i 
# sbatch output.slurm


# sed 's/runSarsaNoOverdrive/runSarsaOriginal/g' output.slurm -i
# sed 's/LsMid/Ls64/g' output.slurm -i
# sed 's/8 2/0 5/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 5/5 5/g' output.slurm -i
# sbatch output.slurm

# sed 's/runSarsaOriginal/runSarsaX/g' output.slurm -i
# sed 's/Ls64/LD200_64/g' output.slurm -i
# sed 's/5 5/0 2/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 2/2 2/g' output.slurm -i 
# sbatch output.slurm
# sed 's/2 2/4 2/g' output.slurm -i 
# sbatch output.slurm
# sed 's/4 2/6 2/g' output.slurm -i 
# sbatch output.slurm
# sed 's/6 2/8 2/g' output.slurm -i 
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