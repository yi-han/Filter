#!/bin/bash
#for dest in punim0621 punim0636; do 
for dest in jpattison; do 
	rsync -avz -e 'ssh' \
	--include=*/ \
	--include='**/*.py' \
	--include='**/*.slurm' \
	--include='**/*.txt' \
	--include='**/*.sh' \
	--include='**/*.apkl' \
	network \
	agent \
	attackSimulations \
	adversary \
	attacks.py \
	experiment.py \
	runDDQN.py \
	runSARSA.py \
	mapsAndSettings.py \
	topologies \
	exp_gpgpu_light.slurm \
	exp_gpgpu_single.slurm \
	exp_gpgpu_heavy.slurm \
	exp_physical.slurm \
	exp_physical_ddqn.slurm \
	exp_either_heavy.slurm \
	exp_either.slurm \
	exp_temp.slurm \
	phys_attempt.slurm \
	cloud_copy.slurm \
	helloWorld.py \
	slurms_cloud_standard.sh \
	slurms_cloud_heavy.sh \
	slurms_physical_standard.sh \
	slurms_physical_heavy.sh \
	slurms_gpgpu_standard.sh \
	slurms_AIMD.sh \
	slurms_gpgpu_latter.sh \
	slurms_gpgpu_v2.sh \
	slurms_gpgpu_v3.sh \
	slurms_physical_v2.sh \
	slurms_ddqn_physical.sh \
	move_files.sh \
	runDDQNNetQuick.py \
	runDDQNMalialis.py \
	runDDQNHundred.py \
	runSarsaNoOverdrive.py \
	runSarsaOriginal.py \
	runSarsaDDQNCopy.py \
	runSarsaX.py \
	runSarsaY.py \
	runSarsaZ.py \
	runAttacks.py \
	runDDQNAdditional.py \
	runSarsaAdditional.py \
	slurms_attacks.sh \
	grid_test.py \
	--exclude='*' \
	jpattison@spartan.hpc.unimelb.edu.au:/home/$dest
	#jpattison@spartan.hpc.unimelb.edu.au:/data/projects/$dest #punim0621
	#jpattison@spartan.hpc.unimelb.edu.au:/data/projects/punim0636  punim0621
done

# jpattison@spartan.hpc.unimelb.edu.au:/home/jpattison/Filter


# rsync -avz -e 'ssh' \
# --include '*/*.py' \
# network \
# agent \
# experiment.py \
# --exclude '*'
# jpattison@spartan.hpc.unimelb.edu.au:/home/jpattison/Filter