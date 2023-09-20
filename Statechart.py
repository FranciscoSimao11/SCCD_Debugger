from Transition import *

class Statechart():
    def __init__(self, initialState, states):
             self.initialState = initialState
             self.states = states

    def addState(self, newState):
        self.states[newState.name] = newState

    def getPrintableStates(self):
        states = ''
        for each in self.states.values():
            states += each.getPrintableObject()
        return states

    def getPrintableObject(self):
        return "Statechart with initial state '{}'\n\nStates:\n\n{}".format(self.initialState, self.getPrintableStates())