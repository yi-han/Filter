import sys
import distributions
import network.hosts as hostClass
assert(len(sys.argv)>=3)


conAttack = hostClass.ConstantAttack
shortPulse = hostClass.ShortPulse
mediumPulse = hostClass.MediumPulse
largePulse = hostClass.LargePulse
gradualIncrease = hostClass.GradualIncrease


directory = sys.argv[1]
repetitions = int(sys.argv[2])

if len(sys.argv)==4:
    name = sys.argv[3]
else:
    name = None

reward_types = ["reward"]

attackClasses = [conAttack, shortPulse, mediumPulse,
    largePulse, gradualIncrease]


testAttacks = True
num_episodes =  60000 #190000


if not testAttacks:
    distributions.distributions(directory, repetitions, num_episodes) #190000
    distributions.reward_graph(directory, attackName, repetitions, name)
else:
    for attackType in attackClasses:
        attackName = "reward-test-{0}".format(attackType.getName())
        distributions.distributions(directory, repetitions, 0, attackName) #190000
        distributions.reward_graph(directory, attackName, repetitions, name)
