import numpy as np
from connect4 import *

def test():
    
    game = Game()
    game.rows = 6
    game.cols = 7
    game.wins = 4
    game.turn = 1
    game.mat = np.zeros((game.rows, game.cols))
    
    # ***************** first test ***************** #
    if check_move(game,0,False): 
        print("test 1: OK !")
    else: 
        print("test 1: Fail !")
    
    # ***************** second test ***************** #
    if not check_move(game,0,True): 
        print("test 2: OK !")
    else: 
        print("test 2: Fail !")
        
    # ***************** third test ***************** #
    game_board_test3 = [[ 1,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]]
    game = apply_move(game,0,False)
    if (game_board_test3 == game.mat).all() : 
        print("test 3: OK !")
    else: 
        print("test 3: Fail !")
    
    # ***************** fourth test ***************** #
    if check_victory(game) == 0:
        print("test 4: OK !")
    else: 
        print("test 4: Fail !")
        
        
test()