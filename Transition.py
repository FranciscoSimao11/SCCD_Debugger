class Transition():
    def __init__(self, target, event, after):
             self.target = target
             self.event = event
             self.after = after

    def getPrintableObject(self):
        return "Transition with Target: {}; Event: {}; After: {};".format(self.target, self.event, self.after)