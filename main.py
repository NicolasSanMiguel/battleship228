# import numpy as np
# from battleship import Ship
import battleship

from random import randint
import os
import random
import numpy as np
# from battleship228.believer import calc_belief
import believer

import matplotlib.pyplot as plt
# # to call a function in battleship.py
# out = battleship.print_board(board_array)

# # to call a class in battleship.py
# out = battleship.Ship(inputs)


def main(row_size, col_size, num_ships, max_ship_size, min_ship_size):
    # Settings Variables
    # row_size = 1 #number of rows
    # col_size = 6 #number of columns
    # num_ships = 1
    # max_ship_size = 3
    # min_ship_size = 3
    # num_turns = row_size * col_size + 1 # number of turns is  greater  than total number of grid spaces

    # Create lists
    ship_list = []

    g = battleship.Game(row_size, col_size, num_ships, max_ship_size, min_ship_size, ship_list)

    # Create the ships

    temp = 0
    while temp < num_ships:
        ship_info = battleship.random_location(g)
        if ship_info == 'None':
            continue
        else:
            g.ship_list.append(
                battleship.Ship(ship_info['size'], ship_info['orientation'], ship_info['location'], g.row_size,
                                g.col_size, g.board, g.board_display))
            temp += 1
    del temp

    # Play Game
    #    os.system('clear')
    #    battleship.print_board(g.board_display, g)

    # initialize the belief state - first choice is random
    belief_state = believer.init_belief(g, 'random')
    #    print('this is init belief state:\n',belief_state)
    guessed = []
    hit = []
    miss = []
    burning_ship = []  # list containing (or not) coordinate that are in a ship that is hit but not sunked
    for turn in range(g.num_turns):
        #        print("Turn:", turn + 1, "of", g.num_turns)
        #        print("Ships left:", len(g.ship_list))
        #        print()
        #        print("burning_ship=",burning_ship)

        if turn >= 1:
            #            belief_state = believer.update_belief_state(g,belief_state)
            belief_state = believer.update_belief_state(g, belief_state, hit, miss, burning_ship)

        row2guess, col2guess = believer.choose_next_best_one(belief_state, guessed)

        #        print("row2guess,col2guess=",row2guess+1,col2guess+1)
        guessed.append([row2guess, col2guess])
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
                #                print("Hit!")
                ship_hit = True
                hit.append([row2guess, col2guess])
                g.board_display[guess_coords['row']][guess_coords['col']] = 'X'
                if ship.destroyed():
                    #                    print("Ship Destroyed!")
                    g.ship_list.remove(ship)
                    burning_ship = []  # the ship sunk, so it is not burning anymore
                else:
                    burning_ship = [[row2guess, col2guess]]
                    pass
                break
        if not ship_hit:
            g.board_display[guess_coords['row']][guess_coords['col']] = '*'
            miss.append([row2guess, col2guess])
        #            print("You missed!")

        #        battleship.print_board(g.board_display, g)

        belief_state = believer.remove_from_belief_state(g, belief_state, guess_coords, ship_hit)

        if not g.ship_list:
            break

    # End Game
    if g.ship_list:
        print("Game Over. You ran out of turns")
    else:
        #        print("All the ships are sunk. You win!")
        #        print('you won in this many turns:',turn+1)
        pass

    return turn + 1


if __name__ == '__main__':
    # main(row_size=4,
    #      col_size=4,
    #      num_ships=1,
    #      max_ship_size=3,
    #      min_ship_size=3)

    ##################################################################################################################
    ######################################### THE SECTION BELOW HERE RUNS IT FOR SET ITERATIONS
    # iterations= 1000
    #
    #
    # numruns = np.zeros(iterations)
    # itermean = []
    #
    # running_mean = 0
    # prev_mean = 100
    # for i in range(iterations):
    #     curr_mean = main(row_size = 4,
    #         col_size = 4,
    #         num_ships = 2,
    #         max_ship_size = 3,
    #         min_ship_size = 3)
    #     numruns[i] = curr_mean
    #     running_mean =running_mean + (1/(i+1))*(curr_mean-running_mean)
    #
    #     deltamean = abs(running_mean - prev_mean)
    #     itermean.append(deltamean)
    #     prev_mean = running_mean
    #     print(deltamean)
    #
    # meannum = np.mean(numruns)
    # print('this is the mean',meannum)
    #
    # plt.plot(np.arange(0, iterations)[1:], itermean[1:])
    # plt.xlabel('Iterations')
    # plt.ylabel('Change in mean per iteration [number of turns]')
    # # plt.axis([0, 6, 0, 20])
    # plt.show()

    ##################################################################################################################
    ######################################### BELOW HERE RUNS IT UNTIL CONVERGENGE
    threshold = 0.001
    numruns = []
    itermean = []

    running_mean = 0
    prev_mean = 10
    deltamean = 100
    i = 0

    # the second condition is to prevent it ending prematurely since the mean oscillates so much in the beginning
    while (deltamean > threshold) or (i < 20):
        curr_mean = main(row_size=6,
                         col_size=6,
                         num_ships=2,
                         max_ship_size=3,
                         min_ship_size=3)
        numruns.append(curr_mean)
        running_mean = running_mean + (1 / (i + 1)) * (curr_mean - running_mean)

        deltamean = abs(running_mean - prev_mean)
        itermean.append(deltamean)
        prev_mean = running_mean
        print(deltamean)

        i += 1

    meannum = np.mean(numruns)
    print('this is the mean',meannum)
    print('this is the i',i)

    plt.figure(1,figsize=(14, 5))
    plt.suptitle('Change in iteratively updated mean with stopping threshold 10^-3')

    plt.subplot(121)
    plt.plot(np.arange(0, i)[1:], itermean[1:])
    plt.xlabel('Iterations')
    plt.ylabel('Change in mean per iteration [number of turns]')
    plt.yscale('log')
    plt.grid(axis='y',which='both')
    plt.grid(axis='x',which='major')

    # plt.show()
    plt.subplot(122)

    # plt.figure(2)
    plt.plot(np.arange(0, i)[1:], itermean[1:])
    plt.xlabel('Iterations')
    plt.ylabel('Change in mean per iteration [number of turns]')
    # plt.title('Change in iteratively updated mean with stopping threshold 10^-3')
    plt.grid(axis='y',which='both')
    plt.show()