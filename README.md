# IDA

IDA is the first self learning DDoS penetration tool created as part of my Master's thesis.

It allows researches to evaluate the effectiveness of a proposed defence against an intelligent attacker. Traditionally network evaluation was performed through simulation against common attacks.

Through Deep Reinforcment Learning, IDA learns a policy designed to minimise the effectiveness of the network defender, therefore IDA can be used to provide a defence metric.  

Using a black box design, IDA will adapt to any network defender and learns a tailored attack strategy through network interaction.

IDA was used to evaluate four different network defenders. IDA was seen to match or outperform all common attack strategies that are commonly used for evaluation purposes. IDA identified a new vulnerability in the previously published MARL defender by committing a unique Pulse Attack. 

This repository is designed to allow the user to run IDA to evaluate Yau's Fair Throttle Defender.

A detailed explanation of IDA can be found in the included draft publication or in Chapter 4 of the included thesis.

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

Primary Python Files:

attacks.py - Generates evaluation episodes for each desired network topology

runFairThrottle.py - Initiates IDA evaluation against the Fair Throttle

runAttacks.py - Evaluate a trained model against a network defender

# Run IDA against the Fair Throttle (AIMD)

```bash

python attacks # generate evaluation episodes for testing
python runAimd.py {mapID} 1 # train and run IDA against Fair Throttle
# Replace mapID with an interger between 0 and 2





```