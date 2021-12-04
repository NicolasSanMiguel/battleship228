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
                b[r,c] = random.randint(0,100)*0+1
        b =b / np.sum(b)


    return b

def calc_belief(g):
    rows = g.row_size
    cols = g.col_size

    return

def update_belief_state(g,b,hit,miss,burning_ships):
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
            boolean=True
            if burning_ships!=[]:
                for x in burning_ships:
                    if x not in ghost_ship:
                        boolean=False
            if boolean:
                totalrollout.append(ghost_ship)                

    # calculates all possible vertical ships
    for c in range(cols):
        for i in range( cols-(shiplen-1) ):
            start_idx = [i,c]
            ghost_ship = [[x+i,c] for x in range(shiplen)]
            boolean=True
            if burning_ships!=[]:
                for x in burning_ships:
                    if x not in ghost_ship:
                        boolean=False
            if boolean:
                totalrollout.append(ghost_ship)                

    # removes ships that have an index of value -1 (hit or miss)
    # TODO: change this to differentiate between when there is a hit or a miss
    spent_indices = []
    # print("miss=",miss)
    for r in range(len(b)):
        curr_row_of_b = b[r]
        for a in range(len(curr_row_of_b)):
            if [r,a] in miss:
                # print("r,a=",r,a)
#            if (curr_row_of_b[a] == -2):
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
                    count = -3
            new_row.append(count)
        newb.append(new_row)

    # convert the matrix of counts to probabilities
    newb = np.array(newb)

    # for totalcount, change all negative 1 to 0
    b2count = np.where(newb < -2*0, 0, newb)
    total_count = np.sum(b2count)
    newb_probs = b2count / total_count # correctly normalized, everything should sum to 1 :)

    for r in range(len(newb_probs)):
        curr_row = newb_probs[r]
        for c in range(len(curr_row)):
            val = curr_row[c]
#            if [r,c] in spent_indices:
            if [r,c] in hit or [r,c] in miss:
                newb_probs[r,c] = -4*0
            # print('this is c',c)
    b = newb_probs
    # print('this is newb:',newb)
    # print('this is total_count:',total_count)
    # print('this is newb_probs:',newb_probs)
    # print("b=",b)
    return b

def choose_max_belief(b):
    # input: b, the belief state. A numpy array of belief probabilities that sum to 1
    # returns: row, column of the maximum value
    #
    # print('this is the b:\n',b)
    print("b=",b)
    row, col = np.where(b == np.max(b))
    i=random.randint(0,len(row)-1)
    # print("the choice you should make is:\n",row[i]+1,col[i]+1)
    return row[i], col[i]

def choose_next_best_one(b,already_guessed):
    # print('we are choosing the next best one now')
    # get the next best choice now
    num_row, num_col = np.shape(b)

    tempb = b
    for idx in already_guessed:
        tempb[idx[0], idx[1]] = 0
    row, col = np.where(tempb == np.max(tempb))

    # if len(row) not X:
    #     then
    i=random.randint(0,len(row)-1)
    # print("In truth, the choice you should make is:\n",row[i]+1,col[i]+1)
    return row[i], col[i]

def remove_from_belief_state(g,b,guess_coords,ship_hit):
    if ship_hit:
        b[guess_coords["row"],guess_coords["col"]] = 0.0001*0 -2
    else:
        b[guess_coords["row"],guess_coords["col"]] = -2
    # remaining_spots = g.row_size * g.col_size - turn + 1
    # newb = np.array()

    return b

def R_at_this_state(b,Rhit,Rmiss,idx):
    # current belief state = b
    # the index in the form [r,c]
    curr_prob = b[idx[0],idx[1]]
    R = curr_prob*Rhit + (1-curr_prob)*Rmiss
    return R

def rollout(g, b, hit, miss, gamma, Rhit, Rmiss,burning_ships):
    bprint=False
    rows = g.row_size
    cols = g.col_size

    b_up = update_belief_state(g, b, hit, miss,burning_ships)
    if bprint:print('this is bup in the loop',b_up)

    Q = np.zeros((rows,cols))
    for r in range(rows):
        for c in range(cols):
            bprint=False
            if bprint:print("r,c=",r,c)
            if bprint: print("isnan? ",sum(sum(np.isnan(Q))))
#            if sum(sum(np.isnan(Q)))>0:
#                0/0
            if [r, c] in hit or [r, c] in miss:
                currQ = -1000
            else:
                R = R_at_this_state(b_up, Rhit, Rmiss, [r,c])
                sum_trans_util_hit = 0
                sum_trans_util_miss = 0
                nan_compensator_hit=1
                nan_compensator_miss=1
                for r2 in range(rows):
                    for c2 in range(cols):
                        bprint=False
                        if bprint:print()
                        # reset to the initial state conditions (hit and miss)
                        hit_sim = hit
                        miss_sim = miss
                        # prob it transitions into the next state
                        trans_hit = b_up[r2, c2]
                        trans_miss = 1 - trans_hit


                        # updates the belief state as a simulation,
                        # recalc b as though it's a hit and as though it's a miss
                        b_up_hit = update_belief_state_sim(g, b_up, hit_sim, miss_sim,[r2,c2],'hit')
                        if bprint:print("b_up=",b_up)
                        if bprint:print("hit_sim=",hit_sim)
                        if bprint:print("miss_sim=",miss_sim)
                        if bprint:print("[r2,c2]=",[r2,c2])
                        b_up_miss = update_belief_state_sim(g, b_up, hit_sim, miss_sim,[r2,c2],'miss')

                        # U_next_is_hit = R_at_this_state(b_up_hit, Rhit, Rmiss, [r2, c2])
                        # U_next_is_miss = R_at_this_state(b_up_miss, Rhit, Rmiss, [r2, c2])
                        if bprint:print("b_up_hit=",b_up_hit)
                        if bprint:print("b_up_miss=",b_up_miss)
                        U_next_is_hit = sum_top_n_probs(b_up_hit,3)
                        U_next_is_miss = sum_top_n_probs(b_up_miss,3)
                        if not np.isnan(U_next_is_miss):
                            nan_compensator_miss +=b_up[r2,c2]
                            sum_trans_util_miss += trans_miss * U_next_is_miss
                        if not np.isnan(U_next_is_hit):
                            nan_compensator_hit +=b_up[r2,c2]
                            sum_trans_util_hit += trans_hit * U_next_is_hit
                            
                        if bprint:print("U_next_is_hit=",U_next_is_hit)
                        if bprint:print("trans_miss=",trans_miss)
                        if bprint:print("U_next_is_miss=",U_next_is_miss)
                        sum_trans_util_hit += trans_hit * U_next_is_hit
                currQ = R + gamma * sum_trans_util_hit / nan_compensator_hit + gamma * sum_trans_util_miss / nan_compensator_miss
                if bprint:print("R=",R)
                if bprint:print("gamma=",gamma)
#                print("sum_trans_util=",sum_trans_util)
            Q[r,c] = currQ

    # the Q matrix is all negative due to the negative reward for each turn, so we want to choose the least negative
    # as the next move. The next move assigns 0 to already surveyed spaces, so we have to convert these to all positive
    # values, so it is not overridden by the choose_next_best_one() function assigning a 0 to a location and that
    # being a higher value than all the elements in Q.

    # # to do this, we take the greatest magnitude of a value and add that to every element.
    # # for example if Q = [-9, -7, -2.5], we would take |-9| and add, so we have q_mags = [0, 2, 6.5]
    # maxmagQ = np.max(-1*Q)
    # Q = Q + maxmagQ
    # # newQ isn't probabilities since it doesnt sum to 1, but we can treat it like they are in the function because
    # # choosing a move just looks for the maximum value of it
    # print('this is q coming out of it',Q)
    return Q

def update_belief_state_sim(g,b,hit_sim,miss_sim,newguess,guess_state):
    bprint=False;
    if bprint:print("*****begin updatae belief state sim*****")
    if bprint:print("hit_sim=",hit_sim)
    if bprint:print("miss_sim=",miss_sim)
    # newguess is the state at which we are exploring this expansion
    # guess_state is either hit or miss - we see what belief_state  is
    # in the case it's a hit and in the case it's a miss
    if bprint:print("newguess=",newguess)
    if guess_state is 'hit':
        hit_sim.append(newguess)
    elif guess_state is 'miss':
        miss_sim.append(newguess)
    else:
        print('simulating neither a hit or a miss - something is wrong')

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
    if bprint:print("a:totalrollout=",totalrollout)
    # calculates all possible vertical ships
    for c in range(cols):
        for i in range( cols-(shiplen-1) ):
            start_idx = [i,c]
            ghost_ship = [[x+i,c] for x in range(shiplen)]
            totalrollout.append(ghost_ship)
    if bprint:print("b:totalrollout=",totalrollout)

    # removes ships that have an index of value -1 (hit or miss)
    # TODO: change this to differentiate between when there is a hit or a miss
    spent_indices = []
    # print("miss=",miss_sim)
    for r in range(len(b)):
        curr_row_of_b = b[r]
        for a in range(len(curr_row_of_b)):
            if [r,a] in miss_sim:
                # print("r,a=",r,a)
                ind = [r,a]
                if ind is not []:
                    spent_indices.append(ind)

    #     if this value [r, spent_ind] is in an array in totalrollout, then remove it.!!
    # print('this is totalroll',len(totalrollout))
    to_remove = []
    for a in range(len(totalrollout)):
        item = totalrollout[a]
        for spent_location in spent_indices:

            if spent_location in item:
                to_remove.append(item)
                # print('this item will be removed',item)
    # this line removes all the items in to_remove
    if bprint:print("c:totalrollout=",totalrollout)
    totalrollout = [e for e in totalrollout if e not in to_remove]
    if bprint:print("d:totalrollout=",totalrollout)

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
                    count = -3
            new_row.append(count)
        newb.append(new_row)

    # convert the matrix of counts to probabilities
    newb = np.array(newb)

    # for totalcount, change all negative 1 to 0
    if bprint:print("newb=",newb)
    b2count = np.where(newb < -2*0, 0, newb)
    total_count = np.sum(b2count)
    newb_probs = b2count / total_count # correctly normalized, everything should sum to 1 :)
    if bprint:print("b2count=",b2count)
    if bprint:print("total_count=",total_count)
    if total_count==0:
        total_count=np.nan
    for r in range(len(newb_probs)):
        curr_row = newb_probs[r]
        for c in range(len(curr_row)):
            val = curr_row[c]
#            if [r,c] in spent_indices:
            if [r,c] in hit_sim or [r,c] in miss_sim:
                newb_probs[r,c] = -4*0
            # print('this is c',c)
    b = newb_probs

    #
    if guess_state is 'hit':
        hit_sim.remove(newguess)
    elif guess_state is 'miss':
        miss_sim.remove(newguess)
    else:
        print('simulating neither a hit or a miss - something is wrong')

    if bprint:print("b=",b)
    if bprint:print("*****end updatae belief state sim*****")
    return b

def sum_top_n_probs(b_up, n):
    b_up = b_up.flatten()
    ind = np.argpartition(b_up, -n)[-n:]
    topvals = b_up[ind] # topvals is a 1d array of the n highest probabilities in the belief state

    outR = np.sum(topvals)
    return outR

def convert2beliefstate(g, Q, hit, miss):
    # to convert Q to a belief state, do the following:
    # (1) remove misses and hits -- set to 0
    # (2) normalize - nahhh
    newb_probs = Q

    for r in range(len(newb_probs)):
        curr_row = newb_probs[r]
        for c in range(len(curr_row)):
            val = curr_row[c]
            #            if [r,c] in spent_indices:
            if [r, c] in hit or [r, c] in miss:
                newb_probs[r, c] = -4 * 0
    newb = newb_probs

    b2count = np.where(newb < -2*0, 0, newb)
    total_count = np.sum(b2count)
    newb_probs = b2count / total_count # correctly normalized, everything should sum to 1 :)

    # print('this is b:\n',newb_probs)
    return newb_probs
