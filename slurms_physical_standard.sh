# standard advesary for medium

sed 's/runDDQN/runSARSA/g' exp_gpgpu_single.slurm > output.slurm
sed 's/sampleDDQNText/ddAdvsarConOrig/g' output.slurm -i
sed "s/samplePath/ddAdvsarConOrig/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm


sed 's/runDDQN/runSarsaNoOverdrive/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarAdvsarConOrig/g' output.slurm -i
sed "s/samplePath/sarAdvsarConOrig/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runSarsaAdditional/g' exp_gpgpu_single.slurm > output.slurm
sed 's/sampleDDQNText/ddAdvsarConSinDD/g' output.slurm -i
sed "s/samplePath/ddAdvsarConSinDD/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runSarsaOriginal/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarAdvsarConSinDD/g' output.slurm -i
sed "s/samplePath/sarAdvsarConSinDD/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i
sbatch output.slurm



sed 's/runDDQN/runSarsaDDQNCopy/g' exp_gpgpu_single.slurm > output.slurm
sed 's/sampleDDQNText/ddAdvsarConHier/g' output.slurm -i
sed "s/samplePath/ddAdvsarConHier/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runSarsaX/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarAdvsarConHier/g' output.slurm -i
sed "s/samplePath/sarAdvsarConHier/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i
sbatch output.slurm



sed 's/runDDQN/runDDQN/g' exp_gpgpu_single.slurm > output.slurm
sed 's/sampleDDQNText/ddAdvDdConSin/g' output.slurm -i
sed "s/samplePath/ddAdvDdConSin/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runDDQNHundred/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarAdvDdConSin/g' output.slurm -i
sed "s/samplePath/sarAdvDdConSin/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i
sbatch output.slurm


sed 's/runDDQN/runDDQNAdditional/g' exp_gpgpu_single.slurm > output.slurm
sed 's/sampleDDQNText/ddAdvDdConHier/g' output.slurm -i
sed "s/samplePath/ddAdvDdConHier/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm

sed 's/runDDQN/runDDQNMalialis/g' exp_cloud.slurm > output.slurm
sed 's/sampleDDQNText/sarAdvDdConHier/g' output.slurm -i
sed "s/samplePath/sarAdvDdConHier/g" output.slurm -i 
sed 's/0 2/0 1/g' output.slurm -i
sbatch output.slurm
sed 's/0 1/1 1/g' output.slurm -i
sbatch output.slurm
sed 's/1 1/2 1/g' output.slurm -i
sbatch output.slurm
sed 's/2 1/3 1/g' output.slurm -i
sbatch output.slurm



