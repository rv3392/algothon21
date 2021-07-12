#!/usr/bin/env python

# RENAME THIS FILE WITH YOUR TEAM NAME.

import numpy as np
import math

nInst=100
currentPos = np.zeros(nInst)
POSITION_LIMIT = 10000

# Dummy algorithm to demonstrate function format.
def getMyPosition (prcSoFar):
    global currentPos
    (nins,nt) = prcSoFar.shape
    Y = np.array([51, 53, 93, 76, 83, 54])
    X = np.array([70, 62, 99, 70, 98, 55])
    beta = np.array([0.6005, 1.1487, 1.0485, 1.2367, 7.8041, 2.0210])
    thresh = np.array([0.5, 0.5, 1, 1, 0.75, 0.5])
    # arbPortfolio = prcSoFar[Y][nt - 1] - prcSoFar[X][nt - 1] * beta
    arbPortfolio = []
    for i in range(len(Y)):
        arbPortfolio.append(prcSoFar[Y[i]][nt - 1] - prcSoFar[X[i]][nt - 1] * beta[i])
    print(arbPortfolio)

    rpos = np.zeros(nInst)
    for j in range(len(Y)):
        if currentPos[Y[j]] == 0:
            if arbPortfolio[j] < -thresh[j]:
                # BUY
                highestValue = max(prcSoFar[Y[j]][nt - 1], beta[j] * prcSoFar[X[j]][nt - 1])
                numToBuy = math.floor(POSITION_LIMIT / highestValue)
                rpos[Y[j]] = numToBuy
                rpos[X[j]] = round(-numToBuy*beta[j])
                print("BUY")
            elif arbPortfolio[j] > thresh[j]:
                # SELL
                rpos[Y[j]] = -100
                rpos[X[j]] = round(100 * beta[j])
                print("SELL")
        elif currentPos[Y[j]] > 0:
            if arbPortfolio[j] > 0:
                # LIQUIDATE
                rpos[Y[j]] = -100
                rpos[X[j]] = round(100 * beta[j])
                print("LIQUIDATE")
        elif currentPos[Y[j]] < 0:
            if arbPortfolio[j] < 0:
                # LIQUIDATE
                rpos[Y[j]] = 100
                rpos[X[j]] = round(-100 * beta[j])
                print("LIQUIDATE")

    currentPos += rpos
    # The algorithm must return a vector of integers, indicating the position of each stock.
    # Position = number of shares, and can be positve or negative depending on long/short position.
    return currentPos
