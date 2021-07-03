#!/usr/bin/env python

# RENAME THIS FILE WITH YOUR TEAM NAME.

import numpy as np

nInst=100
currentPos = np.zeros(nInst)

# Dummy algorithm to demonstrate function format.
def getMyPosition (prcSoFar):
    global currentPos
    (nins,nt) = prcSoFar.shape
    Y = 51
    X = 70
    beta = 0.6005
    thresh = 0.5
    arbPortfolio = prcSoFar[Y][nt - 1] - prcSoFar[X][nt - 1] * beta
    print(arbPortfolio)
    rpos = np.zeros(nInst)
    if currentPos[Y] == 0:
        if arbPortfolio < -thresh:
            # BUY
            rpos[Y] = 400
            rpos[X] = round(-400*beta)
            print("BUY")
        elif arbPortfolio > thresh:
            # SELL
            rpos[Y] = -400
            rpos[X] = round(400 * beta)
            print("SELL")
    elif currentPos[Y] > 0:
        if arbPortfolio > 0:
            # LIQUIDATE
            rpos[Y] = -400
            rpos[X] = round(400 * beta)
            print("LIQUIDATE")
    elif currentPos[Y] < 0:
        if arbPortfolio < 0:
            # LIQUIDATE
            rpos[Y] = 400
            rpos[X] = round(-400 * beta)
            print("LIQUIDATE")

    currentPos += rpos
    # The algorithm must return a vector of integers, indicating the position of each stock.
    # Position = number of shares, and can be positve or negative depending on long/short position.
    return currentPos
