# IDA

What is iDA?

This readme is a condensced 

#Contents:
thesis_jpattison.pdf - Thesis submission to the University of Melbourne - Mark 87 - IDA is introduced in Chapter 4
draft_publication.pdf - Draft submission for publication of work to JNCA (in progress)

Folders:
adversary - contains code for IDA and the dumbAttacker
agent - contains code for network defenders
attackSimulations - contains pickle files detailing resource disbrituion for every episode during an evaluation
network - contains logic of the simulator
shell scripts - contains shell scripts and slurm files specific for the HPC where simulations were run in
topologies - contains .txt files directing network structure of each topology 


attacks.py - Generates evaluation episodes for each desired network topology

runAimd
runAttacks.py - For evaluation

# Run IDA against the Fair Throttle (AIMD)

```bash

python attacks # generate evaluation episodes for testing
python runAimd.py 0 1 # runs 





```




To run:

IDA uses a two stage process - the training and evaluation phase.
IDA is trained/evaluated from a network defender, MARL variant defenders require training prior to IDA being run.




ddqn.py: implement DDQN with prioritised experience replay

network_new.py: set up the network; implement the interaction between the agent and the environment, i.e., def step(), def calculate_reward()
