class Attribute():
    def __init__(self, name, _type):
                self.name = name
                self.type = _type
               
    def getPrintableObject(self):
        return "Attribute: {}\n\n".format(self.name)
