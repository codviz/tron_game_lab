import grid_graphics as gg
from human_player import HumanPlayer
from enemy_player import EnemyPlayer


enemy_player_one = EnemyPlayer(55,20,2)
enemy_player_two = EnemyPlayer(30,5,1)
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
    gg.paint((enemy_player_one.x_pos,enemy_player_one.y_pos),'red')
    gg.paint((enemy_player_two.x_pos,enemy_player_two.y_pos),'yellow')
    gg.paint((human_player.x_pos,human_player.y_pos),'blue')

    for i in range (61):
        gg.paint((i,0),'white')
        gg.paint((i,40),'white')

    for i in range(1,40):
        gg.paint((0,i),'white')
        gg.paint((60,i),'white')

    points_occupied.append((enemy_player_one.x_pos,enemy_player_one.y_pos))
    points_occupied.append((enemy_player_two.x_pos,enemy_player_two.y_pos))
    points_occupied.append((human_player.x_pos,human_player.y_pos))
    human_player.update_position()
    enemy_player_one.update_position(points_occupied)
    enemy_player_two.update_position(points_occupied)

    if (enemy_player_one.x_pos,enemy_player_one.y_pos) in points_occupied:
        g['game_on'] = False
    if (enemy_player_two.x_pos,enemy_player_two.y_pos) in points_occupied:
        g['game_on'] = False
    if (human_player.x_pos, human_player.y_pos) in points_occupied:
        g['game_on'] = False

def key_handler(k):
    if k == 'a':
        human_player.change_direction('left')
    if k == 'd':
        human_player.change_direction('right')

for i in range (61):
    points_occupied.append((i,0))
    points_occupied.append((i,40))

for i in range(1,40):
    points_occupied.append((0,i))
    points_occupied.append((60,i))

if __name__ == "__main__":
    play()
