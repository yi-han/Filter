# IDA

IDA is the first self learning DDoS penetration tool created as part of my Master's thesis.

IDA uses Deep Reinforcment Learning to establish a lower boundary of defence effectiveness for a given defender.

Through exploration of different attacking strategies, IDA learns a policy designed to minimise the effectiveness of the network defender.

Using a black box design, IDA can adapt to any network defender and provided network topology to learn a tailored attack strategy through network interaction.

IDA was used to evaluate four different network defenders. When provided the same attacking resources IDA matched or outperformed the most damaging traditional DDoS attack pattern previously used against the defender. IDA identified a new vulnerability in the previously published MARL defender as it was able to investigate uncommon attack patterns.

This repository is designed to allow the user to run IDA to evaluate Yau's Fair Throttle Defender.

A detailed explanation of IDA can be found in the attatched draft publication or in Chapter 4 of the attatched thesis.

# Contents:
thesis_jpattison.pdf - Thesis submission to the University of Melbourne - Mark 87

draft_publication.pdf - Draft submission for publication of work to JNCA (in progress)

Folders:

adversary - contains code for IDA and the dumbAttacker

agent - contains code for network defenders

attackSimulations - contains pickle files detailing resource disbrituion for every episode during an evaluation

network - contains logic of the simulator

shell scripts - contains shell scripts and slurm files specific for the HPC where simulations were run in

topologies - contains .txt files directing network structure of each topology 



attacks.py - Generates evaluation episodes for each desired network topology

runFairThrottle.py - Initiates IDA evaluation against the Fair Throttle

runAttacks.py - Evaluate a trained model against a network defender

# Run IDA against the Fair Throttle (AIMD)

```bash

python attacks # generate evaluation episodes for testing
python runAimd.py {mapID} 1 # train and run IDA against Fair Throttle
# Replace mapID with an interger between 0 and 2





```