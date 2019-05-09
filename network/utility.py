from enum import Enum

EPSILON = 0.0001
INF = 9999999
MbTKb = 1000 # ratio for converting Mb to Kb
KbTMb = 0.001 # ratio for converting Kb to Mb
SECONDS_STANDARD_INTERVAL = 2
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


class AGENT_REWARD_ENUM(Enum):
    overload = 0
    sliding_negative = 1
    packet_logic = 2


### BUCKET CLASSES ###

class MalBucket():
    # this is an alternative bucket based on how I think Malialis did it
    # results align up

    def __init__(self, iterations_between_second, bucket_capacity):
        assert(bucket_capacity == 0)
        self.reset()

    def reset(self):
        self.through_rate = 1 # default through rate
        self.rs = -1 # means not set
        return

    def update_throttle_rate(self, rs, past_node_load):
        self.rs = rs # used for assert checking only
        self.through_rate = self.calcThroughRate(past_node_load, rs)
        # print("updating the throttle rate")

    def calcThroughRate(self, past_node_load, rs):
        # given the load how much to throttle based on Mal Way
        if rs == -1:
            rs = INF

        past_node_load = past_node_load/2 # reduce the load from 2 second to 1 second average

        #rs = MbToKb(rs)

        if rs >= past_node_load:
            through_rate = 1
        else:
            through_rate = rs / past_node_load
            # print("rs = {0} pastNode = {1} through_rate = {2}".format(rs, past_node_load, through_rate))
        return through_rate

    def bucket_flow(self, legal_traffic_in, illegal_traffic_in, rs):
        # Idea we use past_node_load to calculate a fair throttle under assumption it stays same
        # lazy we times rs_per_action by two to reflect 2 seconds
        # note we're undoing the action in AIMD algorithm
        
        #through_rate = self.calcThroughRate(rs_per_action)
        through_rate = self.through_rate
        assert(rs == self.rs)

        legal_through = legal_traffic_in * through_rate
        legal_dropped = legal_traffic_in - legal_through

        illegal_through = illegal_traffic_in * through_rate
        illegal_dropped = illegal_traffic_in - illegal_through

        
        return (legal_through, legal_dropped, illegal_through, illegal_dropped)





class ProperBucket():
    # This actually reflects a leaky bucket. For fairness the bucket capacity is usually 0
    # so it really just enforces a through rate

    def __init__(self, iterations_between_second, bucket_capacity ):
        # to fix error make it call from the defender settings
        self.iterations_between_second = iterations_between_second
        #self.bucket_capacity = bucket_capacity / iterations_between_second
        self.reset()
    def reset(self):
        return
        #self.bucket_list = [] # to ensure FIFO
        #self.bucket_load = 0

    def update_throttle_rate(self, rs, past_node_load):
        return


    def bucket_flow(self, legal_traffic_in, illegal_traffic_in, rs_per_action):
        """
        
        This used to have buckets attatched however I have put asserts 
        to ensure the bucket is never used and changed the logic so never called
        Leaky bucket rate without a bucket!

        Bucket logic
        Current idea:
        All data must add to the bucket first. Only then can we take it out
        Rationale: We're breaking it down to 10ms steps anyway. The memory would include the ram
        
        First calculate out from the bucket.
        Then calculate what to do with new traffic
        """

        #init_load = legal_traffic_in + illegal_traffic_in

        if rs_per_action == -1:
            # No throttle set
            # print("setting throttle is as")
            rs_per_iteration = INF
        else:
            rs_per_iteration = MbToKb(rs_per_action/self.iterations_between_second)


        (legal_through, illegal_through, legal_dropped, illegal_dropped) = self.calc_traffic_through(legal_traffic_in, illegal_traffic_in, rs_per_iteration)



        return (legal_through, legal_dropped, illegal_through, illegal_dropped)

    def calc_traffic_through(self, legal_in, illegal_in, capacity):
        # When we want to pass through a bottle neck and want to know how much didn't make it as well
        # used to be an own function. Now its just calcBottleNeck + didn't make it
        
        incoming_load = legal_in + illegal_in
        (legal_through, illegal_through) = calcBottleNeck(incoming_load, legal_in, illegal_in, capacity)
        legal_dropped = legal_in - legal_through
        illegal_dropped = illegal_in - illegal_through
        
        return (legal_through, illegal_through, legal_dropped, illegal_dropped)


        ### OBSOLETE. Part of bucket_flow

        # print("load {0} total capacity {1} remaining {2}".format(self.bucket_load, self.bucket_capacity, remaining_capacity))
        # print("capacity is {1} whilst incoming load is {0}".format((illegal_traffic_in+legal_traffic_in),remaining_capacity))
        
        """
        1. Always empty the bucket as much as possible.
        2. If there is still capacity allow as much traffic through from incoming
        3. Fill the bucket up

        """



        # # 1. Get as much out of the bucket as we can
        # legal_out, illegal_out = self.empty_bucket(rs_per_iteration)
        # # assert(legal_out ==0) 
        # # assert(illegal_out == 0) # bucket not used
        # rs_remaining = rs_per_iteration - (legal_out + illegal_out)
        
        # if rs_remaining > EPSILON:
        #     # we still have some more we can let out, use it from the incoming traffic
        #     # print("letting traffic right through")
        #     (t_legal_out, t_illegal_out, legal_remaining, illegal_remaining) = self.calc_traffic_through(legal_traffic_in, illegal_traffic_in, rs_remaining)
        #     legal_out += t_legal_out
        #     illegal_out += t_illegal_out
        # else:
        #     # print("Exhausted remaining rs was {0} and delta is {1}".format(rs_remaining, EPSILON))
        #     legal_remaining = legal_traffic_in
        #     illegal_remaining = illegal_traffic_in
        
        # if (legal_remaining + illegal_remaining > EPSILON):
        #     # print("Now adding to bucket")
        #     (legal_dropped, illegal_dropped) = self.add_to_capacity(legal_remaining, illegal_remaining)
        # else:
        #     # print("none for the bucket")
        #     (legal_dropped, illegal_dropped) = (0,0)

             
        # # print("letting through {0} {1} {2} {3}".format(legal_out, legal_dropped, illegal_out, illegal_dropped))
        # final_load = legal_out + illegal_out
        # if(not ((init_load <= final_load + EPSILON) or abs(final_load - rs_per_iteration) < EPSILON)):
        #     print("init_load = {0} final_load = {1} rs = {2}".format(init_load, final_load, rs_per_iteration))
        #     assert(1==2)
        # # else:
        # # print("see another day")

        # # print("\n\n")
        # return (legal_out, legal_dropped, illegal_out, illegal_dropped)


    # def add_bucket(self, legal_in, illegal_in, at_front=False):
    #     assert(1==2) # we shouldn't use the bucket ever
    #     # add to bucket
    #     assert(legal_in >=0)
    #     assert(illegal_in >= 0)

    #     load = (legal_in + illegal_in)
    #     if load < EPSILON:
    #         return #ignore

    #     if at_front:
    #         # only used if we emptied too much
    #         self.bucket_list.insert(0, (legal_in, illegal_in))
    #     else:
    #         self.bucket_list.append((legal_in, illegal_in))
        
    #     self.updateBucketLoad(load, True)
    #     if (self.bucket_load-self.bucket_capacity)>EPSILON:
    #         print("we're over by {0}".format(self.bucket_load-self.bucket_capacity))
    #         assert(1==2)

    # def updateBucketLoad(self, traffic_changed, is_incoming):
    #     assert(1==2)
    #     assert(traffic_changed>0)
    #     if is_incoming:            
    #         self.bucket_load += traffic_changed
    #     else:
    #         self.bucket_load -= traffic_changed
    #         if self.bucket_load <0:
    #             assert(abs(self.bucket_load)<EPSILON)
    #             self.bucket_load = 0
    #     assert((self.bucket_capacity + EPSILON) > self.bucket_load ) # ensure we never overfilled bucket
    

    # def empty_bucket(self, current_rs):
    #     assert(1==2)
    #     # empty bucket to amount of rs or until empty
        
    #     assert(self.bucket_load - self.bucket_capacity < EPSILON)
    #     legal_out = 0
    #     illegal_out = 0
    #     remaining_rs = current_rs
        
    #     while(self.bucket_list and remaining_rs>EPSILON):

    #         # get first item of list
    #         (f_legal, f_illegal) = self.bucket_list.pop(0)            
    #         f_load = (f_legal + f_illegal)
    #         remaining_rs -= f_load # note this will go negative once we hit our limit
            
    #         legal_out += f_legal
    #         illegal_out += f_illegal
    #         self.updateBucketLoad(f_load, False)


    #     (legal_out, illegal_out, legal_overflow, illegal_overflow) = self.calc_traffic_through(legal_out, illegal_out, current_rs)

    #     self.add_bucket(legal_overflow, illegal_overflow, at_front=True)
    #     return (legal_out, illegal_out)


    # def add_to_capacity(self, legal_in, illegal_in):
    #     # we add as much as we can to the bucket and drop the rest.
    #     # NO TRAFFIC SHOULD COME OUT

    #     traffic_in = legal_in + illegal_in
    #     remaining_capacity = self.bucket_capacity - self.bucket_load
    #     assert(remaining_capacity>=0 and traffic_in >= 0)

    #     if(traffic_in<EPSILON):
    #         return (0, 0)


    #     (legal_added, illegal_added, legal_dropped, illegal_dropped) = self.calc_traffic_through(legal_in, illegal_in, remaining_capacity)


    #     if((legal_added + illegal_added-remaining_capacity)>EPSILON):
    #         print("legal_added {0} illegal_added {1} capacity {2} combined {3}".format(legal_added, illegal_added, capacity, legal_added+illegal_added))
    #         assert(1==2)
        
    #     self.add_bucket(legal_added, illegal_added)
    #     return (legal_dropped, illegal_dropped)


def calcBottleNeck(incoming_load, legal_arrived, illegal_arrived, capacity):
    """
    Used for server and buckets
    Assume we have a bottle neck on how much can pass (or be served).
    
    We have an incoming load which equals legal_arrived + illegal_arrived
    and if the incoming load exceeds the capacity then we need to only let some pass
    """
    #TODO: Remove the assert clauses to speed this up
    assert(legal_arrived >= 0)
    assert(illegal_arrived >= 0)
    assert(incoming_load == (legal_arrived+illegal_arrived))

    if incoming_load <= capacity:# + EPSILON):
        return (legal_arrived, illegal_arrived)

    ratio = capacity/incoming_load

    legal_served = legal_arrived * ratio
    illegal_served = illegal_arrived * ratio
    assert(legal_served<=legal_arrived)
    return(legal_served, illegal_served)