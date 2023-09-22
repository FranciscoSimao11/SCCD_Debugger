class Class():
    def __init__(self, name, methods, relationships, defaultClass):
             self.name = name
             self.methods = methods
             self.relationships = relationships
             self.defaultClass = defaultClass

    def addMethod(self, newMethod):
        self.methods.append(newMethod)

    def getPrintableMethods(self):
        met = ''
        for each in self.methods:
            met += each.getPrintableObject()
        return met
    
    def genFile(self):
        f = open(self.name+".py", "w")
        f.write("class {}():\n\n".format(self.name))
        for m in self.methods:
            f.write("   def {}(self):\n".format(m.name))
            f.write("       {}\n\n".format(m.body))
        f.close()

    def getPrintableObject(self):
        return "Class: {}\nMethods:\n{}\n".format(self.name, self.getPrintableMethods())
