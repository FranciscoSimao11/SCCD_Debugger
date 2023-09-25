
class Method():
    def __init__(self, name, body):
             self.name = name
             self.body = body

    def getPrintableObject(self):
        return "{}() with body: {}\n".format(self.name, self.body)