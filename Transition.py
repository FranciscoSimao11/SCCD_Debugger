import sys

class Transition():
    def __init__(self, target, event, after, script):
             self.target = target
             self.event = event
             self.after = after
             self.script = script 

    def getPrintableObject(self):
        return "Transition with Target: {}; Event: {}; After: {}; Script: {};\n".format(self.target, self.event, self.after, self.script)