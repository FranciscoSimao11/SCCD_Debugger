from Transition import *

class State():
    def __init__(self, name, transitions, script):
             self.name = name
             self.transitions = transitions
             self.script = script

    def addTransition(self, newTransition):
        self.transitions.append(newTransition)

    def getPrintableTransitions(self):
        for each in self.transitions:
           trans = ''
           trans += each.getPrintableObject()
           trans += ' || '
        return trans

    def getPrintableObject(self):
        return "State: {}\nTransitions: {}\nScript: {}\n".format(self.name, self.getPrintableTransitions(), self.script)