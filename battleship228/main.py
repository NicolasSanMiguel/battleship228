# import numpy as np
# from battleship import Ship
import battleship

from random import randint
import os
import random


# # to call a function in battleship.py
# out = battleship.print_board(board_array)

# # to call a class in battleship.py
# out = battleship.Ship(inputs)


def main(row_size, col_size, num_ships, max_ship_size, min_ship_size):
    
    #Settings Variables
    # row_size = 1 #number of rows
    # col_size = 6 #number of columns
    # num_ships = 1
    # max_ship_size = 3
    # min_ship_size = 3
    # num_turns = row_size * col_size + 1 # number of turns is  greater  than total number of grid spaces

    #Create lists
    ship_list = []


    g = battleship.Game(row_size, col_size, num_ships, max_ship_size, min_ship_size, ship_list)



    # Create the ships

    temp = 0
    while temp < num_ships:
        ship_info = battleship.random_location(g)
        if ship_info == 'None':
            continue
        else:
            g.ship_list.append(battleship.Ship(ship_info['size'], ship_info['orientation'], ship_info['location'],g.row_size,g.col_size,g.board, g.board_display))
            temp += 1
    del temp

    # Play Game
    os.system('clear')
    battleship.print_board(g.board_display, g)

    for turn in range(g.num_turns):
        print("Turn:", turn + 1, "of", g.num_turns)
        print("Ships left:", len(g.ship_list))
        print()
  
        guess_coords = {}
        while True:
            guess_coords['row'] = battleship.get_row(g)
            guess_coords['col'] = battleship.get_col(g)
            if g.board_display[guess_coords['row']][guess_coords['col']] == 'X' or \
                g.board_display[guess_coords['row']][guess_coords['col']] == '*':
                print("\nYou guessed that one already.")
            else:
                break

        os.system('clear')

        ship_hit = False
        for ship in g.ship_list:
            if ship.contains(guess_coords):
                print("Hit!")
                ship_hit = True
                g.board_display[guess_coords['row']][guess_coords['col']] = 'X'
                if ship.destroyed():
                    print("Ship Destroyed!")
                    g.ship_list.remove(ship)
                break
        if not ship_hit:
            g.board_display[guess_coords['row']][guess_coords['col']] = '*'
            print("You missed!")

        battleship.print_board(g.board_display, g)
  
        if not g.ship_list:
            break

    # End Game
    if g.ship_list:
        print("Game Over. You ran out of turns")
    else:
        print("All the ships are sunk. You win!")


if __name__ == '__main__':
    main(row_size = 6,
         col_size = 6,
         num_ships = 1,
         max_ship_size = 3,
         min_ship_size = 3)
