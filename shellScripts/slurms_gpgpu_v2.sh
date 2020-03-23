# aimd base

sed 's/runDDQN/runAimdJeremy/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/medium_very_hard_single/g' output.slurm -i 
sed "s/samplePath/medium_very_hard_single/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runDDQNAdditional/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/medium_very_hard_double/g' output.slurm -i 
sed "s/samplePath/medium_very_hard_double/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runDDQNHundred/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/team_full_single/g' output.slurm -i 
sed "s/samplePath/team_full_single/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runDDQNMalialis/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/team_full_double/g' output.slurm -i 
sed "s/samplePath/team_full_double/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runDDQNNetQuick/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/medium_optimal_single/g' output.slurm -i 
sed "s/samplePath/medium_optimal_single/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runSarsaAdditional/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/medium_optimal_double/g' output.slurm -i 
sed "s/samplePath/medium_optimal_double/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runSarsaDDQNCopy/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/full_team_hard_single/g' output.slurm -i 
sed "s/samplePath/full_team_hard_single/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runSarsaNoOverdrive/g' exp_either_heavy.slurm > output.slurm
sed 's/sampleDDQNText/full_team_hard_double/g' output.slurm -i 
sed "s/samplePath/full_team_hard_double/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm


