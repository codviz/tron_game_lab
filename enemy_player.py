from human_player import HumanPlayer
from random import randrange, choice

RANDOM_MOVE_PROBABILITY = 5

class EnemyPlayer(HumanPlayer):

    def calculate_distance(self, points_occupied):
          if self.dx == 1 or self.dx == -1:
               distance_left = self.dx
               distance_right = self.dx
               distance_forward = self.dx
               while True:
                    if (self.x_pos + distance_forward, self.y_pos) in points_occupied:
                        break
                    else:
                         distance_forward += self.dx
               while True:
                    if (self.x_pos, self.y_pos - distance_left) in points_occupied:
                         break
                    else:
                         distance_left += self.dx
               while True:
                    if (self.x_pos, self.y_pos + distance_right) in points_occupied:
                         break
                    else:
                         distance_right += self.dx
          else:
               distance_left = self.dy
               distance_right = self.dy
               distance_forward = self.dy
               while True:
                    if (self.x_pos, self.y_pos + distance_forward) in points_occupied:
                        break
                    else:
                         distance_forward += self.dy
               while True:
                    if (self.x_pos + distance_left, self.y_pos) in points_occupied:
                         break
                    else:
                         distance_left += self.dy
               while True:
                    if (self.x_pos - distance_right, self.y_pos) in points_occupied:
                         break
                    else:
                         distance_right += self.dy

          return abs(distance_left), abs(distance_right), abs(distance_forward)

    def update_position(self,points_occupied):

        distance_left,distance_right,distance_forward = self.calculate_distance(points_occupied)

        if distance_left == 1 and distance_right == 1:
             pass
        elif distance_forward == 1 or randrange(100) < RANDOM_MOVE_PROBABILITY:
             if distance_left > distance_right:
                  self.change_direction('left')
             elif distance_right > distance_left:
                  self.change_direction('right')
             else: 
                  self.change_direction(choice(['left','right']))

        self.x_pos += self.dx
        self.y_pos += self.dy
