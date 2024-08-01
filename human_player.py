class HumanPlayer:

    def __init__(self, startx, starty, start_direction):
        self.list_index = start_direction
        self.x_pos = startx
        self.y_pos = starty
        
        #first pair value is dx, second is dy
        self.direction_combinations = [(1,0),(0,1),(-1,0),(0,-1)]

        self.dx = self.direction_combinations[self.list_index][0]
        self.dy = self.direction_combinations[self.list_index][1]

    def update_position(self):
        #every time this method is called, it should update the x_pos and y_pos of this class
        self.x_pos += self.dx
        self.y_pos += self.dy

    def change_direction(self,direction):
        if direction == 'left':
            if self.list_index == 0:
                self.list_index = 3
            else: 
                self.list_index -= 1
        if direction == 'right':
            if self.list_index == 3:
                self.list_index = 0
            else: 
                self.list_index += 1
        self.dx = self.direction_combinations[self.list_index][0]
        self.dy = self.direction_combinations[self.list_index][1]
