from Transition import *

class State():
    def __init__(self, name, transitions):
             self.name = name
             self.transitions = transitions

    def addTransition(self, newTransition):
        self.transitions.append(newTransition)

    def getPrintableTransitions(self):
        trans = ''
        for each in self.transitions:
           trans += each.getPrintableObject()
        return trans

    def getPrintableObject(self):
        return "State: {}\nTransitions: {}\n".format(self.name, self.getPrintableTransitions())