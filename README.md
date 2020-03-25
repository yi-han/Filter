# IDA

IDA is the first self learning DDoS penetration tool. It uses Deep Reinforcment Learning to explore the effect of different traffic attack patterns against a network defender.

The black box design allows IDA to adapt to any defender and provided network topology learning a tailored attacks through network interaction.

IDA was used to evaluate four different network defenders, when compared to traditional evaluation approaches IDA outperformed the effectiveness of commonly used DDOS attacks when given the same resources.

This repository provides a setup allowing the user to use IDA to evaluate the Yau's Fair Throttle Defender.

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

# Run IDA against the Fair Throttle (AKA AIMD)

```bash

python attacks # generate evaluation episodes for testing
python runAimd.py {mapID} 1 # train and run IDA against Fair Throttle
# Replace mapID with an interger between 0 and 2





```