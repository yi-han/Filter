# No Bottle Testing for experiment one
# this is to be run by vmMachine not spartan


# #AIMD


python runAimdMal.py 0 1 aimdMalProper

python runAimdJeremy.py 0 1 aimdJeremyProper

# sarsa

python runSARSA.py 0 3 sarOrig

python runSarsaAdditional.py 0 10 sarOrigLengthened

python runSarsaOriginal.py 0 10 sarHierOriginalReward


python runDDQNHundred.py 0 10 ddHierOrigReward







