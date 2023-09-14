from Transition import *

class State():
    def __init__(self, name, transitions, entryScript, exitScript):
             self.name = name
             self.transitions = transitions
             self.entryScript = entryScript
             self.exitScript = exitScript

    def addTransition(self, newTransition):
        self.transitions.append(newTransition)

    def getPrintableTransitions(self):
        trans = ''
        for each in self.transitions:
           trans += each.getPrintableObject()
        return trans

    def getPrintableObject(self):
        return "State: {}\nTransitions: {}\nEntry script: {}\nExit script: {}\n\n".format(self.name, self.getPrintableTransitions()[:-2], self.entryScript, self.exitScript)