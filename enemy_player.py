from human_player import HumanPlayer

class EnemyPlayer(HumanPlayer):

  def update_position(self):

    self.x_pos += self.dx
    self.y_pos += self.dy
