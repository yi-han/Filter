#!/bin/bash
rsync -avz -e 'ssh' \
--include=*/ \
--include='**/*.py' \
--include='**/*.slurm' \
--include='**/*.txt' \
--include='**/*.sh' \
network \
agent \
run_slups.sh \
experiment.py \
settings.py \
run_multi_core.py \
topologies \
exp_one_node_one_core.slurm \
exp_two_node_one_core.slurm \
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