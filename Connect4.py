import numpy as np
import random, copy
from time import sleep

##################################################
## Miscellaneous Functions
##################################################

# Accept only a fixed set of values as input
def input_fixed(message, valid_values=[]):
    # Display the message
    print(message, end='')
    # Keep trying the following
    while True:
        # Accept an input
        value = input()
        # Check if it is within acceptable range
        # If not, indicate sttrings that can be accepted
        if not value in valid_values:
            valid_strings = '/'.join(valid_values)
            print('Invalid value, select only [' + valid_strings + ']: ', end='')
        # Otherwise, return the valid supplied by user
        else:
            return value

# Accept an integer as input
def input_integer(message, min=None, max=None):
    # Display the message
    print(message, end='')
    # Keep trying the following
    while True:
        try:
            # Attempt to get a value
            value = int(input())
            # less than minimum value, error
            if not min is None and value < min:
                print('Value should be at least ' + str(min) + ', please try again: ', end='')
                continue
            if not max is None and value > max:
                print('Value should be at most ' + str(max) + ', please try again: ', end='')
                continue
            # Valid value obtained, return it
            return value
        except Exception as e:
            print('Invalid value, please try again: ', end='')

##################################################
## Game Implementation
##################################################

class Game:
    mat = None
    rows = 0
    cols = 0
    turn = 0
    wins = 0

def display_board(game):
    # Reverse the row printing (row 0 at bottom)
    for row in reversed(range(game.rows)):
        # print a row separator
        print('-' * (game.cols * 2 + 1))
        for col in range(game.cols):
            # Display current column value (with column separator)
            print('|' + str(int(game.mat[row, col])), end='')
        # Go to the next line after final column separator
        print('|')
    # print an ending row separator
    print('-' * (game.cols * 2 + 1))

def check_victory(game):
    # Check for winning condition for both players
    # For every cell on the board
    for row in range(game.rows):
        for col in range(game.cols):
            # If this is an empty cell, nothing to check
            if game.mat[row, col] == 0:
                continue
            # Try all 8 directions [change delta row and delta column]
            # 8 directions in N, S, E, W, NE, NW, SE, SW
            dr = [1, -1, 0,  0, 1, -1,  1, -1]
            dc = [0,  0, 1, -1, 1, -1, -1,  1]
            for direction in range(8):
                # Assume this direction can give us a win first
                can_win = True
                # Check for N - 1 discs of same player in said direction
                for k in range(1, game.wins):
                    # Find row and column of disc to test
                    test_row = row + k * dr[direction]
                    test_col = col + k * dc[direction]
                    # If the test disc is invalid or belongs to different player
                    if (test_row < 0 or test_row >= game.rows or
                        test_col < 0 or test_col >= game.cols or
                        game.mat[row, col] != game.mat[test_row, test_col]):
                        can_win = False
                # If we can win, then indicate the player that did
                if can_win:
                    return game.mat[row, col]
    # We never won, now check if anything can be done by the current player
    for col in range(game.cols):
        # Check if current player can pop at a column
        if game.mat[0, col] == game.turn:
            return 0
        # Check if current player can insert at a column
        if game.mat[game.rows - 1, col] == 0:
            return 0
    # Otherwise, game has ended in a draw
    return 3
        


def apply_move(game, col, pop):
    # If we are popping
    if pop:
        # shift everything down
        for row in range(0, game.rows - 1):
            game.mat[row, col] = game.mat[row + 1, col]
        # Top of that column must be a zero
        game.mat[game.rows - 1, col] = 0
    # Otherwise if we are adding a new disc
    else:
        # Search from the bottom row to the top
        for row in range(game.rows):
            # If the row in that column is empty
            if game.mat[row, col] == 0:
                # Put a new disc
                game.mat[row, col] = game.turn
                # We are done
                break
    # Pass turn to the other player
    if game.turn == 1:
        game.turn = 2
    elif game.turn == 2:
        game.turn = 1
    # Return new game as output
    return game
    
def check_move(game, col, pop): 
    # Ensure that column is valid
    if col < 0 or col >= game.cols:
        return False
    # If we are not popping, ensure that there is a 0 in that column
    if not pop and game.mat[game.rows - 1, col] != 0:
        return False
    # If we are popping, ensure our own disk is at bottom of column
    if pop and game.mat[0, col] != game.turn:
        return False
    # Otherwise, we are good with the move
    return True

def computer_move(game, level):
    # Level 1: Random column to play
    if level == 1:
        while True:
            # Generate a random column
            col = random.randint(0, game.cols - 1)
            # Randomly decide if we should pop
            threshold = random.randint(0, 1)
            pop = True if threshold == 1 else False
            # If we can insert a disc, go ahead
            if not pop and game.mat[game.rows - 1, col] == 0:
                return (col, pop)
            # If we can remove a disc, go ahead
            if pop and game.mat[0, col] == game.turn:
                return (col, pop)
    # Level 2 opponent
    elif level == 2:
        # Track list of moves to avoid
        avoid_moves = []
        # Try every possible column
        for col in range(game.cols):
            # Consider 2 cases whether we pop or not
            for pop in [False, True]:
                # If the move is valid in the game
                if check_move(game, col, pop):
                    # Create a test game via deep copy
                    test_game = copy.deepcopy(game)
                    # Apply the move in the test game
                    test_game = apply_move(test_game, col, pop)
                    # If this computer player won
                    if check_victory(test_game) == game.turn:
                        # Use this move immediately
                        return (col, pop)
                    # Create a second test game where other player did this move
                    test_game = copy.deepcopy(game)
                    # Find the other player and make it their turn
                    other_player = 1 if game.turn == 2 else 2
                    test_game.turn = other_player
                    # Apply move as the other player
                    test_game = apply_move(test_game, col, pop)
                    # If the other player would win immediately
                    # Note: this doesn't mean it won't produce an empty
                    #       square filled up by an opponent later to win    
                    if check_victory(test_game) == other_player:
                        # If other player was placing a disc
                        if not pop:
                            # Then we must stop them from winning
                            return (col, pop)
                        # Otherwise, we cannot pop the current disc
                        else:
                            avoid_moves.append((col, pop))
        # There is no direct winning move, generate random one (level 1)
        move = computer_move(game, 1)
        # Make sure it is not an avoided move (i.e. popping that column loses)
        while len(avoid_moves) < game.cols and move in avoid_moves:
            move = computer_move(game, 1)
        return move
        
def menu():
    # Create a new game
    game = Game()
    # Display welcome message
    print('\n' + ('#' * 29) + '\n# Welcome to Connect 4 Game #\n' + ('#' * 29))
    # Number of rows in the game matrix
    game.rows = input_integer('Enter number of rows: ', min=4, max=10)
    # Number of columns in the game matrix
    game.cols = input_integer('Enter number of columns: ', min=4, max=10)
    # Now, create a game matrix
    game.mat = np.zeros((game.rows, game.cols))
    # First player goes first always
    game.turn = 1
    # Number of consecutive discs N for winning a game
    game.wins = input_integer('Enter number of consecutive discs for win: ', min=2, max=max(game.rows, game.cols))
    # First player details
    first_player = input_fixed('Enter first player [human/computer]: ', ['human', 'computer'])
    # First player difficulty level
    first_player_difficulty = None
    if first_player == 'computer':
        first_player_difficulty = int(input_fixed('Enter difficulty level [1/2]: ', ['1', '2']))
    # Second player details
    second_player = input_fixed('Enter second player [human/computer]: ', ['human', 'computer'])
    # Second player difficulty level
    second_player_difficulty = None
    if second_player == 'computer':
        second_player_difficulty = int(input_fixed('Enter difficulty level [1/2]: ', ['1', '2']))
    # If there is no victory/draw in the game yet
    while check_victory(game) == 0:
        print(('#' * 19) + "\n# Player " + str(game.turn) + '\'s turn #\n' + ('#' * 19))
        # display the board
        display_board(game)
        # Move details, column and whether we are popping or not
        column, pop = None, None
        # Check if the current player is a human
        is_human = ((game.turn == 1 and first_player == 'human') or
                    (game.turn == 2 and second_player == 'human'))
        # For human players, accept input
        if is_human:
            # Obtain column for the move
            column = input_integer('Enter column for move: ', min=0, max=game.cols - 1)
            # Obtain boolean for whether we should pop or not
            pop = input_fixed('Pop a disc? [Yes/No]: ', ['Yes', 'No'])
            pop = True if pop == 'Yes' else False
        # For computer players
        else:
            # Find the level of this computer player
            level = first_player_difficulty if game.turn == 1 else second_player_difficulty
            # Generate column and whether it is popping (move information)
            column, pop = computer_move(game, level)
        # Check if a move can be applied
        if check_move(game, column, pop):
            # If so, apply the move and obtain new game
            game = apply_move(game, column, pop)
            # For computers
            if not is_human:
                # Indicate the move the computer played
                pop_string = 'popped' if pop else 'added new'
                print('Computer ' + pop_string + ' disc at column ' + str(column))
                # sleep for 1 second for simulating thinking
                sleep(1)
        # Otherwise indicate that move is invalid
        else:
            print('Move is invalid, resetting turn...')

    # If player 1 won, indicate so
    if check_victory(game) == 1:
        print('\nCongratulations, player 1 has won the game!')
    # If player 2 won, indicate so
    elif check_victory(game) == 2:
        print('\nCongratulations, player 2 has won the game!')
    # If players 1 and 2 both draw, indicate so
    elif check_victory(game) == 3:
        print('\nPlayers 1 and 2 have drawn!')
    # Displat final board
    print(('#' * 22) + '\n# Final board layout #\n' + ('#' * 22))
    display_board(game)
    # Display thank you message
    print('\n' + ('#' * 35))
    print('# Thank you for playing Connect 4 #')
    print(('#' * 35) + '\n')

# Comment this to run test.py as required
menu()
