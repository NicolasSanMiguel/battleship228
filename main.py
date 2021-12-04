# import numpy as np
# from battleship import Ship
import battleship

from random import randint
import os
import random
import numpy as np
# from battleship228.believer import calc_belief
import believer

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
#    os.system('clear')
    battleship.print_board(g.board_display, g)

    # initialize the belief state - first choice is random
    belief_state = believer.init_belief(g,'random')
    print('this is init belief state:\n',belief_state)
    guessed=[]
    hit=[]
    miss=[]
    for turn in range(g.num_turns):
        print("Turn:", turn + 1, "of", g.num_turns)
        print("Ships left:", len(g.ship_list))
        print()

        if turn >=1 :

#            belief_state = believer.update_belief_state(g,belief_state)
            belief_state = believer.update_belief_state(g,belief_state,hit,miss)

        row2guess, col2guess = believer.choose_next_best_one(belief_state,guessed)
        print("row2guess,col2guess=",row2guess+1,col2guess+1)
        guessed.append([row2guess,col2guess])
        # these vars ^^ will be fed directly into the game (no humans)
        # after it is working

        # belief_state = believer.calc_belief(g)
            

        guess_coords = {}
        already_guessed = []
#        row2guess, col2guess = believer.choose_next_best_one(belief_state,guessed)
#        guessed.append([row2guess,col2guess]) 
        guess_coords['row'] = row2guess
        guess_coords['col'] = col2guess
#        while True:
#            guess_coords['row'] = row2guess
#            guess_coords['col'] = col2guess
#            already_guessed.append([row2guess, col2guess])
#            # guess_coords['row'] = battleship.get_row(g)
#            # guess_coords['col'] = battleship.get_col(g)
#            if g.board_display[guess_coords['row']][guess_coords['col']] == 'X' or \
#                g.board_display[guess_coords['row']][guess_coords['col']] == '*':
#                print("\nYou guessed that one already.")
#                row2guess, col2guess = believer.choose_next_best_one(belief_state,guessed)
#            else:
#                guessed.append([row2guess,col2guess])               
#                break

#        os.system('clear')

        ship_hit = False
        for ship in g.ship_list:
            if ship.contains(guess_coords):
                print("Hit!")
                ship_hit = True
                hit.append([row2guess,col2guess])
                g.board_display[guess_coords['row']][guess_coords['col']] = 'X'
                if ship.destroyed():
                    print("Ship Destroyed!")
                    g.ship_list.remove(ship)
                break
        if not ship_hit:
            g.board_display[guess_coords['row']][guess_coords['col']] = '*'
            miss.append([row2guess,col2guess])
            print("You missed!")

        battleship.print_board(g.board_display, g)


        belief_state = believer.remove_from_belief_state(g,belief_state,guess_coords,ship_hit)





        if not g.ship_list:
            break

    # End Game
    if g.ship_list:
        print("Game Over. You ran out of turns")
    else:
        print("All the ships are sunk. You win!")
        print('you won in this many turns:',turn+1)

    return turn+1

if __name__ == '__main__':
     main(row_size = 4,
             col_size = 4,
             num_ships = 1,
             max_ship_size = 3,
             min_ship_size = 3)

#    numruns = np.zeros(1000)
#    for i in range(1000):
#        numruns[i] = main(row_size = 6,
#            col_size = 6,
#            num_ships = 2,
#            max_ship_size = 3,
#            min_ship_size = 3)
#    meannum = np.mean(numruns)
#    print('this is the mean',meannum)