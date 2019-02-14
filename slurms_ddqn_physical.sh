# doing all the tests
sed 's/runSARSA/runDDQN/g' exp_physical.slurm > output.slurm
sed "s/samplePath/$1/g" output.slurm -i 
sed 's/sample_sarsa_name/smallSin/g' output.slurm -i 
sed 's/0 5/0 10/g' output.slurm -i 
sed 's/loadAttacks = False/loadAttacks = True/g' runDDQN.py -i
sbatch output.slurm

sed 's/runDDQN/runDDQNAdditional/g' output.slurm -i
sed 's/smallSin/smallMal/g' output.slurm -i
sed 's/loadAttacks = False/loadAttacks = True/g' runDDQNAdditional.py -i
sbatch output.slurm

sed 's/runDDQNAdditional/runDDQNHundred/g' output.slurm -i
sed 's/smallMal/midSin/g' output.slurm -i
sed 's/loadAttacks = False/loadAttacks = True/g' runDDQNHundred.py -i
sbatch output.slurm



sed 's/runDDQNHundred/runDDQNMalialis/g' output.slurm -i
sed 's/midSin/midMal/g' output.slurm -i
sed 's/loadAttacks = False/loadAttacks = True/g' runDDQNMalialis.py -i
sbatch output.slurm


sed 's/runDDQNMalialis/runDDQNNetQuick/g' output.slurm -i
sed 's/midMal/midHier/g' output.slurm -i
sed 's/loadAttacks = False/loadAttacks = True/g' runDDQNNetQuick.py -i
sbatch output.slurm

sed 's/runDDQNNetQuick/runSarsaAdditional/g' output.slurm -i
sed 's/midHier/64Sin/g' output.slurm -i
sed 's/loadAttacks = False/loadAttacks = True/g' runSarsaAdditional.py -i
sbatch output.slurm

sed 's/runSarsaAdditional/runSarsaDDQNCopy/g' output.slurm -i
sed 's/64Sin/64Hier/g' output.slurm -i
sed 's/loadAttacks = False/loadAttacks = True/g' runSarsaDDQNCopy.py -i
sbatch output.slurm

sed 's/runSarsaDDQNCopy/runSarsaNoOverdrive/g' output.slurm -i
sed 's/64Hier/64_50/g' output.slurm -i
sed 's/loadAttacks = False/loadAttacks = True/g' runSarsaNoOverdrive.py -i
sbatch output.slurm

