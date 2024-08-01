import grid_graphics as gg
from human_player import HumanPlayer

human_player = HumanPlayer(5,20,0)
points_occupied = []

#game states dictionary
g = {}

UPDATE_RATE = 100

def play():
    g['game_on'] = True
    gg.open_window(title='Tron Light CyclesGame')
    game_loop()
    gg.set_key_handler(key_handler)
    gg.event_loop()

def game_loop():
     gg.set_timer(game_loop, UPDATE_RATE)
     if g['game_on']:
        update()

def update():
    #method called every loop cycle
    gg.paint((human_player.x_pos,human_player.y_pos),'blue')


def key_handler(k):
    #already enabled, k equals the string value of the key pressed
    pass

if __name__ == "__main__":
    play()
