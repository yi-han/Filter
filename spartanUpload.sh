#!/bin/bash
rsync -avz -e 'ssh' \
--include=*/ \
--include='**/*.py' \
--include='**/*.slurm' \
--include="**/*.txt" \
network \
agent \
experiment.py \
settings.py \
topology.txt \
exp_one_node_one_core.slurm \
--exclude='*' \
jpattison@spartan.hpc.unimelb.edu.au:/home/jpattison/Filter

# jpattison@spartan.hpc.unimelb.edu.au:/home/jpattison/Filter


# rsync -avz -e 'ssh' \
# --include '*/*.py' \
# network \
# agent \
# experiment.py \
# --exclude '*'
# jpattison@spartan.hpc.unimelb.edu.au:/home/jpattison/Filter