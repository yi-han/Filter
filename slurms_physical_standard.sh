# Experiment 2 base

# sbatch  --dependency=afterok:${sJob1##* } output.slurm
# rsync -avz --exclude="*/*.csv" --exclude="*.csv" --exclude="*/*/*.csv" --exclude="*.out"  --include="*" --include="*/*" ../properExpOneMedium/ .

# #AIMD
sed 's/runDDQN/runAimdMal/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/adv_aimdMalProper/g' output.slurm -i 
sed "s/samplePath/adv_aimdMalProper/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
# sed 's/2 1/3 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/3 1/4 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/4 1/5 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/5 1/6 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/6 1/7 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/7 1/8 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/8 1/9 1/g' output.slurm -i
# sbatch output.slurm

sed 's/runDDQN/runAimdJeremy/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/adv_aimdJeremyProper/g' output.slurm -i 
sed "s/samplePath/adv_aimdJeremyProper/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
# sed 's/2 1/3 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/3 1/4 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/4 1/5 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/5 1/6 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/6 1/7 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/7 1/8 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/8 1/9 1/g' output.slurm -i
# sbatch output.slurm

# # standard
sed 's/runDDQN/runSARSA/g' exp_either.slurm > output.slurm
sed 's/sampleDDQNText/adv_sarOrig/g' output.slurm -i 
sed "s/samplePath/adv_sarOrig/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/2 1/3 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/3 1/4 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/4 1/5 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/5 1/6 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/6 1/7 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/7 1/8 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/8 1/9 1/g' output.slurm -i
# sbatch output.slurm


sed 's/runDDQN/runSarsaAdditional/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/adv_sarOrigLengthened/g' output.slurm -i 
sed "s/samplePath/adv_sarOrigLengthened/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
# sed 's/2 1/3 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/3 1/4 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/4 1/5 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/5 1/6 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/6 1/7 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/7 1/8 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/8 1/9 1/g' output.slurm -i
# sbatch output.slurm




sed 's/runDDQN/runSarsaDDQNCopy/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/adv_Sliding_sarSinPackets/g' output.slurm -i 
sed "s/samplePath/adv_Sliding_sarSinPackets/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
# sed 's/2 1/3 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/3 1/4 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/4 1/5 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/5 1/6 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/6 1/7 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/7 1/8 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/8 1/9 1/g' output.slurm -i
# sbatch output.slurm

sed 's/runDDQN/runDDQN/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/adv_ddSingleA/g' output.slurm -i 
sed "s/samplePath/adv_ddSingleA/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
# sed 's/2 1/3 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/3 1/4 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/4 1/5 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/5 1/6 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/6 1/7 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/7 1/8 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/8 1/9 1/g' output.slurm -i
# sbatch output.slurm

sed 's/runDDQN/runDDQNAdditional/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/adv_Sliding_ddSingleA/g' output.slurm -i 
sed "s/samplePath/adv_Sliding_ddSingleA/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
# sed 's/2 1/3 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/3 1/4 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/4 1/5 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/5 1/6 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/6 1/7 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/7 1/8 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/8 1/9 1/g' output.slurm -i
# sbatch output.slurm



sed 's/runDDQN/runDDQNHundred/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/adv_ddHierPackets/g' output.slurm -i 
sed "s/samplePath/adv_ddHierPackets/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
# sed 's/2 1/3 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/3 1/4 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/4 1/5 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/5 1/6 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/6 1/7 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/7 1/8 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/8 1/9 1/g' output.slurm -i
# sbatch output.slurm



