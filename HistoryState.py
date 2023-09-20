from Transition import *

class HistoryState():
    def __init__(self, name, kind, parentState):
            self.name = name
            self.kind = kind
            self.lastState = None
            self.parentState = parentState
            self.transitions = []
            
    def setupTransitions(self):
        for s in parentState.childState:
            newTransition = Transition(s.name, None, 0, None)
            self.transitions.append(newTransition)
                    
    def isHistoryState(self):
        return True
    
    def isComposite(self):
        return False
    
    def getPrintableObject(self):
        return "History State: {} with type {}\n\n".format(self.name, self.kind)