#!/bin/bash
for dest in punim0621 punim0636; do 
	rsync -avz -e 'ssh' \
	--include=*/ \
	--include='**/*.py' \
	--include='**/*.slurm' \
	--include='**/*.txt' \
	--include='**/*.sh' \
	network \
	agent \
	attacks.py \ß
	experiment.py \
	runDDQN.py \
	runSARSA.py \
	mapsAndSettings.py \
	topologies \
	exp_gpgpu_single.slurm \
	exp_cloud.slurm \
	phys_attempt.slurm \
	helloWorld.py \
	slurms_cloud_standard.sh \
	slurms_gpgpu_standard.sh \
	--exclude='*' \
	jpattison@spartan.hpc.unimelb.edu.au:/data/projects/$dest #punim0621
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