# Experiment 2 base

# sbatch  --dependency=afterok:${sJob1##* } output.slurm


# sed 's/runDDQN/runSARSA/g' exp_either.slurm > output.slurm
# sed 's/sampleDDQNText/adv_sarOrig/g' output.slurm -i 
# sed "s/samplePath/adv_sarOrig/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i
# sbatch output.slurm


# sed 's/runDDQN/runSarsaAdditional/g' exp_either_heavy.slurm > output.slurm
# sed 's/sampleDDQNText/adv_Sliding_sarOrig/g' output.slurm -i 
# sed "s/samplePath/adv_Sliding_sarOrig/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i
# sbatch output.slurm

# sed 's/runDDQN/runSarsaDDQNCopy/g' exp_either.slurm > output.slurm
# sed 's/sampleDDQNText/adv_sarSinNor/g' output.slurm -i 
# sed "s/samplePath/adv_sarSinNor/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i
# sbatch output.slurm



# sed 's/runDDQN/runSarsaNoOverdrive/g' exp_either_heavy.slurm > output.slurm
# sed 's/sampleDDQNText/adv_Sliding_sarSinNor/g' output.slurm -i 
# sed "s/samplePath/adv_Sliding_sarSinNor/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i
# sbatch output.slurm

# sed 's/runDDQN/runSarsaOriginal/g' exp_either.slurm > output.slurm
# sed 's/sampleDDQNText/adv_sarSinPackets/g' output.slurm -i 
# sed "s/samplePath/adv_sarSinPackets/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i
# sbatch output.slurm

# sed 's/runDDQN/runSarsaX/g' exp_either_heavy.slurm > output.slurm
# sed 's/sampleDDQNText/adv_Sliding_sarSinPackets/g' output.slurm -i 
# sed "s/samplePath/adv_Sliding_sarSinPackets/g" output.slurm -i 
# sed 's/0 2/0 3/g' output.slurm -i
# sbatch output.slurm


# sed 's/runDDQN/runSarsaY/g' exp_either.slurm > output.slurm
# sed 's/sampleDDQNText/adv_sarHierNorm/g' output.slurm -i 
# sed "s/samplePath/adv_sarHierNorm/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i
# sbatch output.slurm

# sed 's/runDDQN/runSarsaZ/g' exp_either.slurm > output.slurm
# sed 's/sampleDDQNText/adv_sarHierPackets/g' output.slurm -i 
# sed "s/samplePath/adv_sarHierPackets/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i
# sbatch output.slurm



# sed 's/runDDQN/runDDQN/g' exp_either_heavy.slurm > output.slurm
# sed 's/sampleDDQNText/adv_ddSinNorm/g' output.slurm -i 
# sed "s/samplePath/adv_ddSinNorm/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i
# sbatch output.slurm

# sed 's/runDDQN/runDDQNAdditional/g' exp_either_heavy.slurm > output.slurm
# sed 's/sampleDDQNText/adv_ddSinPackets/g' output.slurm -i 
# sed "s/samplePath/adv_ddSinPackets/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i
# sbatch output.slurm

# sed 's/runDDQN/runDDQNHundred/g' exp_either_heavy.slurm > output.slurm
# sed 's/sampleDDQNText/adv_ddHierNorm/g' output.slurm -i 
# sed "s/samplePath/adv_ddHierNorm/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i
# sbatch output.slurm

# sed 's/runDDQN/runDDQNMalialis/g' exp_either_heavy.slurm > output.slurm
# sed 's/sampleDDQNText/adv_ddHierPackets/g' output.slurm -i 
# sed "s/samplePath/adv_ddHierPackets/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i
# sbatch output.slurm

# # No Throttle
# sed 's/runDDQN/runDDQNNetQuick/g' exp_either.slurm > output.slurm
# sed 's/sampleDDQNText/adv_noThrottle/g' output.slurm -i 
# sed "s/samplePath/adv_noThrottle/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i
# sbatch output.slurm


# AIMD
# sed 's/runDDQN/runAimdMal/g' exp_either.slurm > output.slurm
# sed 's/sampleDDQNText/adv_aimdMal/g' output.slurm -i 
# sed "s/samplePath/adv_aimdMal/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i
# sbatch output.slurm

# sed 's/runDDQN/runAimdJeremy/g' exp_either.slurm > output.slurm
# sed 's/sampleDDQNText/adv_aimdJeremy/g' output.slurm -i 
# sed "s/samplePath/adv_aimdJeremy/g" output.slurm -i 
# sed 's/0 2/0 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/0 1/1 1/g' output.slurm -i
# sbatch output.slurm
# sed 's/1 1/2 1/g' output.slurm -i
# sbatch output.slurm

