from Transition import *

class Statechart():
    def __init__(self, initialState, states):
             self.initialState = initialState
             self.states = states

    def addState(self, newState):
        self.states[newState.name] = newState

    def getPrintableStates(self):
        trans = ''
        for each in self.states.values():
            trans += each.getPrintableObject()
        return trans

    def getPrintableObject(self):
        return "Statechart with initial state {}\n\nStates:\n{}".format(self.initialState, self.getPrintableStates())