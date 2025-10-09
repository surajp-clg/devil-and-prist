class RiverBank:
    def __init__(self,priest,devil):
        left_bank = []
        right_bank = []
        devil_lt = 0
        priest_lt = 0 
        devil_rt = 0
        priest_rt = 0
        half_of_char = len(priest)
        win = False

        # Counting characters on left and right sides of the river bank
        for i in range(len(priest)):
            if priest[i].get_side()==0:
                right_bank.append(priest[i])
            else:
                left_bank.append(priest[i])
            
            if devil[i].get_side()==0:
                right_bank.append(devil[i])
            else:
                left_bank.append(devil[i])

            
        # Get count of Devils and priests 
        for person in left_bank:
            if person.is_devil():
                devil_lt += 1
            else:
                priest_lt += 1  

        for person in right_bank:
            if person.is_devil():
                devil_rt += 1
            else:
                priest_rt += 1     
    
    def game_state(self):
        self.is_running = True
        # Lose Condition
        if (self.devil_lt > self.priest_lt and self.priest_lt > 0) or (self.devil_rt > self.priest_rt and self.priest_rt > 0):
            self.is_running = False

        # Win Condition
        elif self.devil_lt == self.half_of_char and self.priest_lt == self.half_of_char:
            self.is_running = False
            self.win = True
        return self.is_running
    
    def Result(self):
        return self.win

        


    


