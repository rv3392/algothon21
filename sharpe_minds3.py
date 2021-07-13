#!/usr/bin/env python

# RENAME THIS FILE WITH YOUR TEAM NAME.

import numpy as np
import math

nInst=100
currentPos = np.zeros(nInst)
POSITION_LIMIT = 10000

histArbPortfolio = []
for x in range(6):
    histArbPortfolio.append([])


def exp_ma(prices, days, smoothing=2):
    ema = [sum(prices[:days]) / days]
    for price in prices[days:]:
        ema.append((price * (smoothing / (1 + days))) + ema[-1] * (1 - (smoothing / (1 + days))))
    return ema


def getMyPosition (prcSoFar):
    global currentPos
    (nins,nt) = prcSoFar.shape
    # Y = np.array([51, 53, 93, 76, 83, 54])
    # X = np.array([70, 62, 99, 70, 98, 55])
    # beta = np.array([0.6005, 1.1487, 1.0485, 1.2367, 7.8041, 2.0210])
    # thresh = np.array([0.5, 0.5, 1, 1, 0.75, 0.5])

    Y = np.array([56, 69, 80, 57, 84, 63])
    X = np.array([98, 79, 66, 71, 91, 51])
    beta = np.array([6.1422, 3.8933, 1.2849, 0.5559, 0.1984, 1.7626])
    thresh = np.array([0.39, 0.85, 0.32, 0.4, 0.0889, 0.84])

    arbPortfolio = []
    for i in range(len(Y)):
        arbPortfolio.append(prcSoFar[Y[i]][nt - 1] - prcSoFar[X[i]][nt - 1] * beta[i])
    # print(arbPortfolio)

    rpos = np.zeros(nInst)
    for j in range(len(Y)):
        histArbPortfolio[j].append(arbPortfolio[j])
        # print(histArbPortfolio)
        bias = exp_ma(histArbPortfolio[j], 20, 1)[-1] if len(histArbPortfolio[j]) >= 20 else 0
        # print(bias)

        if currentPos[Y[j]] == 0:
            highestValue = max(prcSoFar[Y[j]][nt - 1], beta[j] * prcSoFar[X[j]][nt - 1])
            numToBuy = math.floor(POSITION_LIMIT / highestValue)
            if arbPortfolio[j] < -thresh[j] + bias:
                # BUY
                rpos[Y[j]] = numToBuy
                rpos[X[j]] = round(-numToBuy*beta[j])
                print("BUY")
            elif arbPortfolio[j] > thresh[j] + bias:
                # SELL
                rpos[Y[j]] = -numToBuy
                rpos[X[j]] = round(numToBuy * beta[j])
                print("SELL")
        elif currentPos[Y[j]] > 0:
            if arbPortfolio[j] > 0 + bias:
                # LIQUIDATE
                rpos[Y[j]] = -currentPos[Y[j]]
                rpos[X[j]] = -currentPos[X[j]]
                print("LIQUIDATE")
        elif currentPos[Y[j]] < 0:
            if arbPortfolio[j] < 0 + bias:
                # LIQUIDATE
                rpos[Y[j]] = -currentPos[Y[j]]
                rpos[X[j]] = -currentPos[X[j]]
                print("LIQUIDATE")

    currentPos += rpos
    # The algorithm must return a vector of integers, indicating the position of each stock.
    # Position = number of shares, and can be positve or negative depending on long/short position.
    return currentPos