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

# def update_belief_state_hit(g,b):
#     return b

def update_belief_state(g,b):
    # given a belief state, do one step rollout
    # first assuming one 3-unit ship
    # print('THIS IS B:\n',b)
    # game plan:
    # 1. for a given nxn board, calculate the size possible orientations for the boat and
    # store the indicies for each of those ship orientations in a list
    # 2. take the indices of unavailable units (DIFF B/W UNAVAIL B/C HIT/MISS)
    # and remove ineligible ones from the list
    # 3. go through and count number of occurances of each index -> get a matrix of
    # counts for each unexplored position
    # 4. convert the counts to a probability for each location

    rows = g.row_size
    cols = g.col_size
    shiplen = 3
    # find all ways a 3 unit ship can be horizontally placed on a row
    # for each row, = rowlength - (shiplength-1)


    totalrollout = []
    # calculates all possible horizontal ships
    for r in range(rows):
        for i in range( rows-(shiplen-1) ):
            start_idx = [r,i]
            ghost_ship = [[r,x+i] for x in range(shiplen)]
            totalrollout.append(ghost_ship)

    # calculates all possible vertical ships
    for c in range(cols):
        for i in range( cols-(shiplen-1) ):
            start_idx = [i,c]
            ghost_ship = [[x+i,c] for x in range(shiplen)]
            totalrollout.append(ghost_ship)

    # removes ships that have an index of value -1 (hit or miss)
    # TODO: change this to differentiate between when there is a hit or a miss
    spent_indices = []
    for r in range(len(b)):
        curr_row_of_b = b[r]
        for a in range(len(curr_row_of_b)):
            if (curr_row_of_b[a] == -1):
                ind = [r,a]
                if ind is not []:
                    spent_indices.append(ind)

    #     if this value [r, spent_ind] is in an array in totalrollout, then remove it.!!
    # print('this is totalroll',len(totalrollout))
    to_remove = []
    for a in range(len(totalrollout)):
        item = totalrollout[a]
        for spent_location in spent_indices:
            # print('this is spent location',spent_location)
            # print('this is item',item)

            if spent_location in item:
                to_remove.append(item)
                # print('this item will be removed',item)
    # this line removes all the items in to_remove
    totalrollout = [e for e in totalrollout if e not in to_remove]

    # create a matrix of counts
    newb = []
    for r in range(rows):
        new_row = []
        for c in range(cols):
            count = 0
            curr_index = [r,c]
            # go thru each ship in totalrollout and count occurrances of this index
            for ghost in totalrollout:
                # print('this is ghost',ghost)
                # print('this is curr index',curr_index)
                if curr_index in ghost:
                    count += 1
                elif curr_index in spent_indices: # idk if ill end up needing this - otherwise, it just sets already hit spaces to 0
                    count = -1
            new_row.append(count)
        newb.append(new_row)

    # convert the matrix of counts to probabilities
    newb = np.array(newb)

    # for totalcount, change all negative 1 to 0
    b2count = np.where(newb == -1, 0, newb)
    total_count = np.sum(b2count)
    newb_probs = b2count / total_count # correctly normalized, everything should sum to 1 :)

    for r in range(len(newb_probs)):
        curr_row = newb_probs[r]
        for c in range(len(curr_row)):
            val = curr_row[c]
            if [r,c] in spent_indices:
                newb_probs[r,c] = -1
            # print('this is c',c)
    b = newb_probs
    # print('this is newb:',newb)
    # print('this is total_count:',total_count)
    # print('this is newb_probs:',newb_probs)

    return b

def choose_max_belief(b):
    # input: b, the belief state. A numpy array of belief probabilities that sum to 1
    # returns: row, column of the maximum value
    #
    # print('this is the b:\n',b)
    row, col = np.where(b == np.max(b))
    print("the choice you should make is:\n",row[0]+1,col[0]+1)
    return row[0], col[0]

def choose_next_best_one(b,already_guessed):
    # print('we are choosing the next best one now')
    # get the next best choice now
    tempb = b
    for idx in already_guessed:
        tempb[idx[0], idx[1]] = 0
    row, col = np.where(tempb == np.max(tempb))
    return row[0], col[0]


def remove_from_belief_state(g,b,guess_coords,ship_hit):
    if ship_hit:
        b[guess_coords["row"],guess_coords["col"]] = 0.0001
    else:
        b[guess_coords["row"],guess_coords["col"]] = -1
    # remaining_spots = g.row_size * g.col_size - turn + 1
    # newb = np.array()

    return b



