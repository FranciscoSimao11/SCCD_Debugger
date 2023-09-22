class Misc():
    def __init__(self, author, modelName, top, inport, outport, description):
                self.author = author
                self.modelName = modelName
                self.top = top
                self.inport = inport
                self.outport = outport
                self.description = description

    def getPrintableObject(self):
        return "Model: {}\n\n".format(self.modelName)
