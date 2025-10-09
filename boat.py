class Boat:
    def __init__(self):
        self.boat_side = 0
        self.capacity = 2
        self.passengers = []
    
    def add_passenger(self, character):
        if len(self.passengers) < self.capacity and character.get_side() == self.boat_side:
            character.is_on_boat = True
            self.passengers.append(character)
        

    def remove_passenger(self, character):
        if character in self.passengers:
            character.is_on_boat = False
            character.side = self.boat_side
            self.passengers.remove(character)
    
    def boat_move(self):
        if len(self.passengers) > 0:
            self.boat_side = 1 if self.boat_side==0 else 0
            for i in self.passengers:
                i.move()