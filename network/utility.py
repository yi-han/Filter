from enum import Enum

DELTA = 0.001
INF = 9999999
MbTKb = 1000 # ratio for converting Mb to Kb
KbTMb = 0.001 # ratio for converting Kb to Mb

ATTACK_START = 10 # the number of seconds before an attack can start in evaluation

ROUND_SPOT = 6
def KbToMb(kb):
    return kb*KbTMb

def MbToKb(mb):
    return mb*MbTKb

def roundNumber(number):
    # we had a lot of floating point stuff going on so hopefully we can fix that.
    return number
    return round(number, 6)

def round_half_down(n, decimals=5):
    return n
    multiplier = 10 ** decimals
    return math.ceil(n*multiplier - 0.5) / multiplier


def clip(min_value, max_value, value):
    if value < min_value:
        return min_value
    elif value > max_value:
        return max_value
    else:
        return value

# def deep_copy_state(state):
#     state_copy = np.empty_like(state)
#     state_copy[:] = state
#     return state_copy

class advesaryStandardAttackEnum(Enum):
    constant = 0
    pulse_short = 1 
    pulse_medium = 2
    pulse_large = 3
    gradual = 4
    split = 5
    random = 6

