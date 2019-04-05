#!/bin/sh

# dd adv. Exp2


origName="sarOrig"
prefix="ddAdv"
newName="$prefix$origName"

sJob1=$(sbatch cloud_copy.slurm $1 $origName $newName)


echo "waiting for $sJob1"
sed "s/runDDQN/runSARSA/g" exp_cloud.slurm > output.slurm
sed "s/sampleDDQNText/$newName/g" output.slurm -i
sed "s/samplePath/$newName/g" output.slurm -i 
sed "s/0 2/0 1/g" output.slurm -i
sbatch  --dependency=afterok:${sJob1##* } output.slurm 
sed "s/0 1/1 1/g" output.slurm -i
sbatch  --dependency=afterok:${sJob1##* } output.slurm 
sed "s/1 1/2 1/g" output.slurm -i
sbatch  --dependency=afterok:${sJob1##* } output.slurm 
sed "s/2 1/3 1/g" output.slurm -i
sbatch  --dependency=afterok:${sJob1##* } output.slurm 
sed "s/3 1/4 1/g" output.slurm -i
sbatch  --dependency=afterok:${sJob1##* } output.slurm 



origName="sarSinDD"
prefix="ddAdv"
newName="$prefix$origName"
sJob2=$(sbatch cloud_copy.slurm $1 $origName $newName)


sed "s/runDDQN/runSarsaAdditional/g" exp_cloud.slurm > output.slurm
sed "s/sampleDDQNText/$newName/g" output.slurm -i
sed "s/samplePath/$newName/g" output.slurm -i 
sed "s/0 2/0 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob2##* } output.slurm
sed "s/0 1/1 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob2##* } output.slurm
sed "s/1 1/2 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob2##* } output.slurm
sed "s/2 1/3 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob2##* } output.slurm
sed "s/3 1/4 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob2##* } output.slurm

origName="sarSinDdMemory"
prefix="ddAdv"
newName="$prefix$origName"
sJob3=$(sbatch cloud_copy.slurm $1 $origName $newName)

sed "s/runDDQN/runSarsaDDQNCopy/g" exp_cloud.slurm > output.slurm
sed "s/sampleDDQNText/$newName/g" output.slurm -i
sed "s/samplePath/$newName/g" output.slurm -i 
sed "s/0 2/0 2/g" output.slurm -i
sbatch --dependency=afterok:${sJob3##* } output.slurm
sed "s/0 2/0 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob3##* } output.slurm
sed "s/0 1/1 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob3##* } output.slurm
sed "s/1 1/2 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob3##* } output.slurm
sed "s/2 1/3 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob3##* } output.slurm
sed "s/3 1/4 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob3##* } output.slurm

origName="sarHier"
prefix="ddAdv"
newName="$prefix$origName"
sJob4=$(sbatch cloud_copy.slurm $1 $origName $newName)

sed "s/runDDQN/runSarsaNoOverdrive/g" exp_cloud.slurm > output.slurm
sed "s/sampleDDQNText/$newName/g" output.slurm -i
sed "s/samplePath/$newName/g" output.slurm -i 
sed "s/0 2/0 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob4##* } output.slurm
sed "s/0 1/1 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob4##* } output.slurm
sed "s/1 1/2 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob4##* } output.slurm
sed "s/2 1/3 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob4##* } output.slurm
sed "s/3 1/4 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob4##* } output.slurm

origName="sarHierMem"
prefix="ddAdv"
newName="$prefix$origName"
sJob5=$(sbatch cloud_copy.slurm $1 $origName $newName)
sed "s/runDDQN/runSarsaOriginal/g" exp_cloud.slurm > output.slurm
sed "s/sampleDDQNText/$newName/g" output.slurm -i
sed "s/samplePath/$newName/g" output.slurm -i 
sed "s/0 2/0 2/g" output.slurm -i
sbatch --dependency=afterok:${sJob5##* } output.slurm
sed "s/0 2/0 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob5##* } output.slurm
sed "s/0 1/1 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob5##* } output.slurm
sed "s/1 1/2 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob5##* } output.slurm
sed "s/2 1/3 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob5##* } output.slurm
sed "s/3 1/4 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob5##* } output.slurm

origName="ddSin"
prefix="ddAdv"
newName="$prefix$origName"
sJob6=$(sbatch cloud_copy.slurm $1 $origName $newName)

sed "s/runDDQN/runDDQN/g" exp_cloud.slurm > output.slurm
sed "s/sampleDDQNText/$newName/g" output.slurm -i
sed "s/samplePath/$newName/g" output.slurm -i 
sed "s/0 2/0 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob6##* } output.slurm
sed "s/0 1/1 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob6##* } output.slurm
sed "s/1 1/2 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob6##* } output.slurm
sed "s/2 1/3 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob6##* } output.slurm
sed "s/3 1/4 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob6##* } output.slurm



origName="ddSinMem"
prefix="ddAdv"
newName="$prefix$origName"
sJob7=$(sbatch cloud_copy.slurm $1 $origName $newName)

sed "s/runDDQN/runDDQNAdditional/g" exp_cloud.slurm > output.slurm
sed "s/sampleDDQNText/$newName/g" output.slurm -i
sed "s/samplePath/$newName/g" output.slurm -i 
sed "s/0 2/0 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob7##* } output.slurm
sed "s/0 1/1 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob7##* } output.slurm
sed "s/1 1/2 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob7##* } output.slurm
sed "s/2 1/3 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob7##* } output.slurm
sed "s/3 1/4 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob7##* } output.slurm



origName="ddHier"
prefix="ddAdv"
newName="$prefix$origName"
sJob8=$(sbatch cloud_copy.slurm $1 $origName $newName)

sed "s/runDDQN/runDDQNHundred/g" exp_cloud.slurm > output.slurm
sed "s/sampleDDQNText/$newName/g" output.slurm -i
sed "s/samplePath/$newName/g" output.slurm -i 
sed "s/0 2/0 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob8##* } output.slurm
sed "s/0 1/1 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob8##* } output.slurm
sed "s/1 1/2 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob8##* } output.slurm
sed "s/2 1/3 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob8##* } output.slurm
sed "s/3 1/4 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob8##* } output.slurm


origName="ddHierMem"
prefix="ddAdv"
newName="$prefix$origName"
sJob9=$(sbatch cloud_copy.slurm $1 $origName $newName)

sed "s/runDDQN/runDDQNMalialis/g" exp_cloud.slurm > output.slurm
sed "s/sampleDDQNText/$newName/g" output.slurm -i
sed "s/samplePath/$newName/g" output.slurm -i 
sed "s/0 2/0 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob9##* } output.slurm
sed "s/0 1/1 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob9##* } output.slurm
sed "s/1 1/2 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob9##* } output.slurm
sed "s/2 1/3 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob9##* } output.slurm
sed "s/3 1/4 1/g" output.slurm -i
sbatch --dependency=afterok:${sJob9##* } output.slurm



