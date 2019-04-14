# mucking

sed 's/runDDQN/runSARSA/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/ddAdvSarOrigSmall/g' output.slurm -i 
sed "s/samplePath/ddAdvSarOrigSmall/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/2 1/3 1/g' output.slurm -i
# sbatch output.slurm

sed 's/runDDQN/runSarsaAdditional/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/ddAdvSarOrig64/g' output.slurm -i 
sed "s/samplePath/ddAdvSarOrig64/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/2 1/3 1/g' output.slurm -i
# sbatch output.slurm



# sed 's/runDDQN/runDDQN/g' exp_cloud.slurm > output.slurm
# sed 's/sampleDDQNText/ddMalSmall/g' output.slurm -i 
# sed "s/samplePath/ddMalSmall/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/2 1/3 1/g' output.slurm -i
# sbatch output.slurm

