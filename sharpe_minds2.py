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

    if nt % 100 == 0:
        P = np.zeros((100, 100))
        for i in range(100):
            for j in range(100):
                _, p_value, _ = ts.coint(prcSoFar[i, :], df[j, :])
                P[i, j] = p_value

        n = 5
        np.fill_diagonal(P, 1)
        P_flat = P.flatten()
        index = np.argsort(P_flat)
        pairs = []
        candidates = []

        count = 0
        for idx in index[:500]:
            i = idx // 100
            j = idx - i * 100
            if i not in candidates and j not in candidates:
                pairs.append((i, j))
                candidates.append(i)
                candidates.append(j)

                    ount += 1
            if count >= n:
                break

    Y = np.array([i for i, _ in pairs])
    X = np.array([j for _, j in pairs])
    
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
            highestValue = max(prcSoFar[Y[j]][nt - 1], beta[j] * prcSoFar[X[j]][nt - 1])
            numToBuy = math.floor(POSITION_LIMIT / highestValue)
            if arbPortfolio[j] < -thresh[j]:
                # BUY
                rpos[Y[j]] = numToBuy
                rpos[X[j]] = round(-numToBuy*beta[j])
                print("BUY")
            elif arbPortfolio[j] > thresh[j]:
                # SELL
                rpos[Y[j]] = -numToBuy
                rpos[X[j]] = round(numToBuy * beta[j])
                print("SELL")
        elif currentPos[Y[j]] > 0:
            if arbPortfolio[j] > 0:
                # LIQUIDATE
                rpos[Y[j]] = -currentPos[Y[j]]
                rpos[X[j]] = -currentPos[X[j]]
                print("LIQUIDATE")
        elif currentPos[Y[j]] < 0:
            if arbPortfolio[j] < 0:
                # LIQUIDATE
                rpos[Y[j]] = -currentPos[Y[j]]
                rpos[X[j]] = -currentPos[X[j]]
                print("LIQUIDATE")

    currentPos += rpos
    # The algorithm must return a vector of integers, indicating the position of each stock.
    # Position = number of shares, and can be positve or negative depending on long/short position.
    return currentPos