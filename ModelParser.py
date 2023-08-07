from State import *
from Transition import *

class ModelParser():

    # def __init__(self):
    #          self.states = []
    

    def parseModel(self, file):
        states = []
        for each in file:
            line = each.strip()
            if "<state id" in line:                
                parts = line.split(' ')
                stateId = parts[1][4:-2]
                state = State(stateId, [], '')
                currState = state
                states.append(state)
            elif "<transition" in line:
                parts = line.split(' ')
                target = ''
                event = ''
                after = ''
                for each in parts:
                    if "target" in each:
                        target = each[11:-1] #8
                    elif "event" in each:
                        event = each[7:-1]
                    elif "after" in each:
                        after = each[7:-1]
                transition = Transition(target, event, after)
                currState.addTransition(transition)
        return states
