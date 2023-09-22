from Transition import *

class State():
    def __init__(self, name, transitions, entryScript, exitScript, initialState, childStates, parentState, parallel):
             self.name = name
             self.transitions = transitions
             self.entryScript = entryScript
             self.exitScript = exitScript
             self.initialState = initialState #its only an id
             self.childStates = childStates
             self.parentState = parentState
             self.parallel = parallel

    def addTransition(self, newTransition):
        self.transitions.append(newTransition)
        
    def addState(self, newState):
        self.childStates[newState.name] = newState
        
    def isComposite(self):
        return self.initialState != None
    
    def isHistoryState(self):
        return False
    
    def isParallel(self):
        return parallel

    def getPrintableCollection(self, collection):
        trans = '' 
        for each in collection:
            trans += each.getPrintableObject()
        return trans
    
    def getPrintableObject(self):
        composite = 'Yes' if self.isComposite() else 'No\n'
        printableStates = '' if composite != 'Yes' else '\nChild States:\n\n' + self.getPrintableCollection(self.childStates.values())
        return "State: {}\nTransitions: {}\nEntry script: {}\nExit script: {}\nComposite State: {} {}\n".format(self.name, self.getPrintableCollection(self.transitions)[:-2], self.entryScript, self.exitScript, composite, printableStates)