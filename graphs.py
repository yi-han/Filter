import sys
import distributions
sys.path.insert(0, '/Users/jeremypattison/LargeDocument/researchProject/Filter/network')
import hosts as hostClass
assert(len(sys.argv)>=3)


conAttack = hostClass.ConstantAttack
shortPulse = hostClass.ShortPulse
mediumPulse = hostClass.MediumPulse
largePulse = hostClass.LargePulse
gradualIncrease = hostClass.GradualIncrease

randomNotGradual = hostClass.CoordinatedRandom

directory = sys.argv[1]
repetitions = int(sys.argv[2])

if len(sys.argv)==4:
    name = sys.argv[3]
else:
    name = None

reward_types = ["reward"]

attackClasses = [conAttack, shortPulse, mediumPulse,
    largePulse, gradualIncrease]


testAttacks = False
averageFrom =  60000 #90000 #60000 #190000


if not testAttacks:
    for attackType in [conAttack]:
        attackName = "reward-save-{0}".format(attackType.getName())
        distributions.distributions(directory, repetitions, averageFrom, attackName) #190000
        distributions.reward_graph(directory, attackName, repetitions, name)
        distributions.reward_graph(directory, attackName, repetitions, PerLegitTraffic = True, title = "\% Legit Traffic")
        distributions.distributions(directory, repetitions, averageFrom, attackName, PerLegitTraffic = True) #190000

else:
    for attackType in attackClasses:
        attackName = "reward-test-{0}".format(attackType.getName())
        distributions.distributions(directory, repetitions, averageFrom, attackName) #190000
        distributions.reward_graph(directory, attackName, repetitions, name)
