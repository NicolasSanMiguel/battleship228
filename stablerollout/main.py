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
    bprint=False
    bprintgrid=False
    #Settings Variables
    # row_size = 1 #number of rows
    # col_size = 6 #number of columns
    # num_ships = 1
    # max_ship_size = 3
    # min_ship_size = 3
    # num_turns = row_size * col_size + 1 # number of turns is  greater  than total number of grid spaces

    # algorithm settings
    gamma = 0.5 # gamma for the discout factor (rollout)
    Rhit = 1 # reward for hit (rollout and MCTS)
    Rmiss = -1 # reward for miss (rollout and MCTS)

    c = 4 # exploration parameter for the UCB1 heuristic (MCTS)



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
#    if bprint:battleship.print_board(g.board_display, g)
#    battleship.print_board(g.board_display, g)
    # initialize the belief state - first choice is random
    belief_state = believer.init_belief(g,'random')
    if bprint:print('this is init belief state:\n',belief_state)
    guessed=[]
    hit=[]
    miss=[]
    burning_ships=[]
    for turn in range(g.num_turns):
        if bprint:battleship.print_board(g.board_display, g)
        if bprintgrid:battleship.print_board(g.board_display, g)
        if bprint:print("Turn:", turn + 1, "of", g.num_turns)
        if bprint:print("Ships left:", len(g.ship_list))
        if bprint:print()
        if turn >=1 :
            # # this is for the regular one-step lookahead
            # belief_state = believer.update_belief_state(g,belief_state,hit,miss)

            # this is for the rollout
            if bprint:print('beliefstate BEFORE Q:', belief_state)
            Q = believer.rollout(g,belief_state,hit,miss,gamma,Rhit,Rmiss,burning_ships)
            if bprint:print('beliefstate AFTER Q:', Q)

            belief_state = believer.convert2beliefstate(g,Q,hit,miss)
            if bprint:print('beliefstate AFTER CONVERSION:',belief_state)


        row2guess, col2guess = believer.choose_next_best_one(belief_state,guessed)
        # print("row2guess,col2guess=",row2guess+1,col2guess+1)
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
                if bprint:print("Hit!")
                ship_hit = True
                hit.append([row2guess,col2guess])
                g.board_display[guess_coords['row']][guess_coords['col']] = 'X'
                if ship.destroyed():
                    if bprint:print("Ship Destroyed!")
                    g.ship_list.remove(ship)
                    burning_ships=[]
                else:
                    burning_ships.append([row2guess,col2guess])
                break
        if not ship_hit:
            g.board_display[guess_coords['row']][guess_coords['col']] = '*'
            miss.append([row2guess,col2guess])
            if bprint:print("You missed!")

        if bprint:battleship.print_board(g.board_display, g)
        if bprintgrid:battleship.print_board(g.board_display, g)
        if bprint:print('beliefstate BEFORE:',belief_state)
        belief_state = believer.remove_from_belief_state(g,belief_state,guess_coords,ship_hit)
        if bprint:print('beliefstate AFTER:',belief_state)





        if not g.ship_list:
            break

    # End Game
    if g.ship_list:
        print("Game Over. You ran out of turns")
        pass
    else:
        if bprint:print("All the ships are sunk. You win!")
        if bprint:print('you won in this many turns:',turn+1)
        pass

    return turn+1

if __name__ == '__main__':
        # main(row_size = 4,
        #      col_size = 4,
        #      num_ships = 1,
        #      max_ship_size = 3,
        #      min_ship_size = 3)
        nbruns=100
        numruns = np.zeros(nbruns)
        for i in range(nbruns):
            if i % 100 == 0:
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! this is run: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',i)
            numruns[i] = main(row_size = 4,
                col_size = 4,
                num_ships = 2,
                max_ship_size = 3,
                min_ship_size = 3)
        print('this is the mean', np.mean(numruns))
