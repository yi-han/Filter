sed 's/runDDQN/runSARSA/g' exp_physical_ddqn.slurm > temp1.slurm
sed 's/sampleDDQNText/64Dqn100lSin/g' temp1.slurm > temp2.slurm
sed 's/sampleDDQNText/64Dqn100Sin/g' temp1.slurm > output.slurm
# sbatch temp2.slurm
# sleep 30
sed 's/0 2/0 1/g' temp2.slurm > output.slurm
sbatch output.slurm
# sed 's/0 2/4 2/g' temp2.slurm > output.slurm
# sbatch output.slurm
# sed 's/0 2/6 2/g' temp2.slurm > output.slurm
# sbatch output.slurm
# sed 's/0 2/8 2/g' temp2.slurm > output.slurm
# sbatch output.slurm
# sed 's/0 2/10 2/g' temp2.slurm > output.slurm
# sbatch output.slurm
# sed 's/0 2/12 2/g' temp2.slurm > output.slurm
# sbatch output.slurm
# sed 's/0 2/14 2/g' temp2.slurm > output.slurm
# sbatch output.slurm
# sed 's/0 2/16 2/g' temp2.slurm > output.slurm
# sbatch output.slurm
# sed 's/0 2/18 2/g' temp2.slurm > output.slurm
# sbatch output.slurm
