class Association():
    def __init__(self, name, className, min_, max_):
                self.name = name
                self.className = className
                self.min = min_
                self.max = max_
                
    def getPrintableObject(self):
        return "Association: {} to class {}\n\n".format(self.name, self.className)
