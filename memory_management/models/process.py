class Process:

    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.status = "Waiting"
        self.location = None


    def allocate(self, location):
        self.status = "Allocated"
        self.location = location


    def __str__(self):
        return f"{self.name} - {self.size}KB"