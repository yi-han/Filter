# exp3
# cp -R ../$1/ddConSin e3DdAdvDdSinDef
# cp -R ../$1/ddConHier e3DdAdvDdHierDef
# cp -R ../$1/sarConSinDD e3DdAdvSarSinDef
# cp -R ../$1/sarConHier e3DdAdvSarHierDef
# rm */*.csv

# cp -R e3DdAdvDdSinDef e3SarAdvDdSinDef
# cp -R e3DdAdvDdHierDef e3SarAdvDdHierDef
# cp -R e3DdAdvSarSinDef e3SarAdvSarSinDef
# cp -R e3DdAdvSarHierDef e3SarAdvSarHierDef


# sed 's/runDDQN/runDDQN/g' exp_gpgpu_single.slurm > output.slurm
# sed 's/sampleDDQNText/e3DdAdvDdSinDef/g' output.slurm -i 
# sed "s/samplePath/e3DdAdvDdSinDef/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm



# sed 's/runDDQN/runDDQNAdditional/g' exp_physical_ddqn.slurm > output.slurm
# sed 's/sampleDDQNText/e3SarAdvDdSinDef/g' output.slurm -i 
# sed "s/samplePath/e3SarAdvDdSinDef/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/2 1/3 1/g' output.slurm -i 
# sbatch output.slurm

# sed 's/runDDQN/runDDQNHundred/g' exp_gpgpu_single.slurm > output.slurm
# sed 's/sampleDDQNText/e3DdAdvDdHierDef/g' output.slurm -i 
# sed "s/samplePath/e3DdAdvDdHierDef/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm


# sed 's/runDDQN/runDDQNMalialis/g' exp_physical_ddqn.slurm > output.slurm
# sed 's/sampleDDQNText/e3SarAdvDdHierDef/g' output.slurm -i 
# sed "s/samplePath/e3SarAdvDdHierDef/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/2 1/3 1/g' output.slurm -i 
# sbatch output.slurm

sed 's/runDDQN/runSARSA/g' exp_gpgpu_single.slurm > output.slurm
sed 's/sampleDDQNText/e3DdAdvSarSinDef/g' output.slurm -i 
sed "s/samplePath/e3DdAdvSarSinDef/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm


sed 's/runDDQN/runSarsaAdditional/g' exp_physical_ddqn.slurm > output.slurm
sed 's/sampleDDQNText/e3SarAdvSarSinDef/g' output.slurm -i 
sed "s/samplePath/e3SarAdvSarSinDef/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i 
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i 
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i 
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i 
sbatch output.slurm


# sed 's/runDDQN/runSarsaDDQNCopy/g' exp_gpgpu_single.slurm > output.slurm
# sed 's/sampleDDQNText/e3DdAdvSarHierDef/g' output.slurm -i 
# sed "s/samplePath/e3DdAdvSarHierDef/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm


# sed 's/runDDQN/runSarsaNoOverdrive/g' exp_physical_ddqn.slurm > output.slurm
# sed 's/sampleDDQNText/e3SarAdvSarHierDef/g' output.slurm -i 
# sed "s/samplePath/e3SarAdvSarHierDef/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i 
# sbatch output.slurm
# sed 's/2 1/3 1/g' output.slurm -i 
# sbatch output.slurm