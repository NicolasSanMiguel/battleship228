# Nicolas San Miguel and Jacques Verzat
# AA 228 Fall 2021 

import numpy as np
import random
import os

# import  other files
import battleship


def init_belief(g,tag):
    b = np.zeros((g.row_size,g.col_size))

    if tag is 'random':
        # make each entry random
        for r in range(g.row_size):
            for c in range(g.col_size):
                b[r,c] = random.randint(0,100)
        b =b / np.sum(b)


    return b

def calc_belief(g):
    rows = g.row_size
    cols = g.col_size

    return

def update_belief_state(g,b):
    return b

def choose_max_belief(b):
    # input: b, the belief state. A numpy array of belief probabilities that sum to 1
    # returns: row, column of the maximum value
    #
    print('this is the b:\n',b)
    row, col = np.where(b == np.max(b))
    print("the choice you should make is:\n",row[0]+1,col[0]+1)
    return row[0], col[0]

def remove_from_belief_state(g,b,guess_coords,turn):
    b[guess_coords["row"],guess_coords["col"]] = 0
    # remaining_spots = g.row_size * g.col_size - turn + 1
    # newb = np.array()

    return b



