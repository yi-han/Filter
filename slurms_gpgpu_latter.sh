# mucking

sed 's/runDDQN/runSARSA/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarsaOrigSmall/g' output.slurm -i 
sed "s/samplePath/sarsaOrigSmall/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runSarsaAdditional/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarsaDdqnLinSmall/g' output.slurm -i 
sed "s/samplePath/sarsaDdqnLinSmall/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i
sbatch output.slurm



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

