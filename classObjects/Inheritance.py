class Inheritance():
    def __init__(self, name, priority):
                self.name = name
                self.priority = priority

    def getPrintableObject(self):
        return "Inheritance: {}\n\n".format(self.name)
