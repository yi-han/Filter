#!/bin/bash
# standard advesary tests

sed 's/runDDQN/runSARSA/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/Test_ddAdvsarConOrig/g' output.slurm -i
sed "s/samplePath/ddAdvsarConOrig/g" output.slurm -i 
sed 's/0 2/0 2/g' output.slurm -i
sbatch --dependency=afterany:7696161,7696162 output.slurm

#sbatch --dependency=afterany:7696161,7696162

sed 's/runDDQN/runSarsaNoOverdrive/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/Test_sarAdvsarConOrig/g' output.slurm -i
sed "s/samplePath/sarAdvsarConOrig/g" output.slurm -i 
sed 's/0 2/0 4/g' output.slurm -i
sbatch --dependency=afterany:7696161,7696162 output.slurm

sed 's/runDDQN/runSarsaAdditional/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/Test_ddAdvsarConSinDD/g' output.slurm -i
sed "s/samplePath/ddAdvsarConSinDD/g" output.slurm -i 
sed 's/0 2/0 2/g' output.slurm -i
sbatch --dependency=afterany:7696161,7696162 output.slurm


sed 's/runDDQN/runSarsaOriginal/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/Test_sarAdvsarConSinDD/g' output.slurm -i
sed "s/samplePath/sarAdvsarConSinDD/g" output.slurm -i 
sed 's/0 2/0 4/g' output.slurm -i
sbatch --dependency=afterany:7696161,7696162 output.slurm



sed 's/runDDQN/runSarsaDDQNCopy/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/Test_ddAdvsarConHier/g' output.slurm -i
sed "s/samplePath/ddAdvsarConHier/g" output.slurm -i 
sed 's/0 2/0 2/g' output.slurm -i
sbatch --dependency=afterany:7696161,7696162 output.slurm


sed 's/runDDQN/runSarsaX/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/Test_sarAdvsarConHier/g' output.slurm -i
sed "s/samplePath/sarAdvsarConHier/g" output.slurm -i 
sed 's/0 2/0 4/g' output.slurm -i
sbatch --dependency=afterany:7696161,7696162 output.slurm



sed 's/runDDQN/runDDQN/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/Test_ddAdvDdConSin/g' output.slurm -i
sed "s/samplePath/ddAdvDdConSin/g" output.slurm -i 
sed 's/0 2/0 2/g' output.slurm -i
sbatch --dependency=afterany:7696161,7696162 output.slurm


sed 's/runDDQN/runDDQNHundred/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/Test_sarAdvDdConSin/g' output.slurm -i
sed "s/samplePath/sarAdvDdConSin/g" output.slurm -i 
sed 's/0 2/0 4/g' output.slurm -i
# sed 's/0 2/0 2/g' output.slurm -i
sbatch --dependency=afterany:7696161,7696162 output.slurm


sed 's/runDDQN/runDDQNAdditional/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/Test_ddAdvDdConHier/g' output.slurm -i
sed "s/samplePath/ddAdvDdConHier/g" output.slurm -i 
sed 's/0 2/0 2/g' output.slurm -i
sbatch --dependency=afterany:7696161,7696162 output.slurm


sed 's/runDDQN/runDDQNMalialis/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/Test_sarAdvDdConHier/g' output.slurm -i
sed "s/samplePath/sarAdvDdConHier/g" output.slurm -i 
sed 's/0 2/0 4/g' output.slurm -i
sbatch --dependency=afterany:7696161,7696162 output.slurm



