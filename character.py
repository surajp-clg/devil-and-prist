class Charecter:
    def __init__(self):
        self.side = 0
        self.id = 0
        self.is_devil = False
        self.is_on_boat = False

    def get_side(self):
        return self.side
    
    def move(self):
        if self.side == 0:
            self.side = 1
        else:
            self.side = 0

class devil(Charecter):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.is_devil = True
        print("devil : ", self.id)

class priest(Charecter):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.is_devil = False
        print("priest : ", self.id)