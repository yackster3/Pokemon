import numpy as np
from matplotlib import pyplot as plt
import math
"""
Various Exp growth rates in Pokemon, there are 6 growth rates where the amount of experience
required to reach level X is function(x), thus exp to level up is function(x1)-function(x0)
"""
def fast(x):
    return 4*(x**3)/5

def mediumFast(x):
    return x**3

def mediumSlow(x):
    return 6*(x**3)/5 - 15*(x**2)+100*x-140

def erratic(x):
    if x <= 50:
        return (x**3)*(100-x)/50
    elif x <= 68:
        return (x**3)*(150-x)/100
    elif x<=98:
        return (x**3)*math.floor((1911-10*x)/3)/500
    else:
        return (x**3)*(160-x)/100

def fluctuating(x):
    if x<=15:
        return (x**3)*(math.floor((x+1)/3)+24)/50
    elif x<=36:
        return (x**3)*(x+14)/50
    elif x<=100:
        return (x**3)*(math.floor(x/2)+32)/50

def slow(x):
    return 5*x**3/4


def expRequired(minimum = 1, maximum = 100, include = ["Fast", "Medium Fast", "Medium Slow", "Erratic", "Fluctuating", "Slow"]):
    #Get the span of the levels you want to plot
    N = maximum-minimum
    x = np.linspace(minimum, maximum, N)
    ERR = []
    FLU = []
    for i in x:
        myInt = int(i)
        err = erratic(myInt)
        ERR.append(err)

        flu = fluctuating(myInt)
        FLU.append(flu)

    #Get the amount of EXP required to level up at each level.
    if "Fast" in include:
        plt.plot(x, fast(x), label = "Fast")
    if "Medium Fast" in include:
        plt.plot(x, mediumFast(x), label = "Medium Fast")
    if "Medium Slow" in include:
        plt.plot(x, mediumSlow(x), label = "Medium Slow")
    if "Erratic" in include:
        plt.plot(x, ERR, label = "Erratic")
    if "Fluctuating" in include:
        plt.plot(x, FLU, label = "Fluctuating")
    if "Slow" in include:
        plt.plot(x, slow(x), label = "Slow")

    #Plot details
    plt.legend()
    plt.xlabel("Level")
    plt.ylabel("Exp Required")
    plt.show()
    return

def levelUp(minimum = 1, maximum = 100, include = ["Fast", "Medium Fast", "Medium Slow", "Erratic", "Fluctuating", "Slow"]):
    #Get the span of the levels you want to plot
    N = maximum-minimum
    x = np.linspace(minimum, maximum, N)

    fst = []
    mfst = []
    mslw = []
    err = []
    flu = []
    slw = []

    #Get the amount of EXP required to level up
    for i in range(1, len(x)):
        if "Fast" in include:
            fst.append(fast(x[i])-fast(x[i-1]))
        if "Medium Fast" in include:
            mfst.append(mediumFast(x[i])-mediumFast(x[i-1]))
        if "Medium Slow" in include:
            mslw.append(mediumSlow(x[i])-mediumSlow(x[i-1]))
        if "Erratic" in include:
            err.append(erratic(x[i]) - erratic(x[i-1]))
        if "Fluctuating" in include:
            flu.append(fluctuating(x[i]) - fluctuating(x[i-1]))
        if "Slow" in include:
            slw.append(slow(x[i])- slow(x[i-1]))

    #Drop the first element of the array
    x = x[1:]

    #Plot the EXP groups you want to see
    if "Fast" in include:
        plt.plot(x, fst, label = "Fast")
    if "Medium Fast" in include:
        plt.plot(x, mfst, label = "Medium Fast")
    if "Medium Slow" in include:
        plt.plot(x, mslw, label = "Medium Slow")
    if "Erratic" in include:
        plt.plot(x, err, label = "Erratic")
    if "Fluctuating" in include:
        plt.plot(x, flu, label = "Fluctuating")
    if "Slow" in include:
        plt.plot(x, slw, label = "Slow")

    #Plot details
    plt.legend()
    plt.xlabel("Level")
    plt.ylabel("Exp Required")
    plt.show()
    return


def otherStat(base, lv, IV = 0, EV = 0):
    return math.floor((((base + IV)*2 + math.ceil(np.sqrt(EV)/4))*lv)/100) + 5

def hpStat(base, lv, IV = 0, EV = 0):
    return otherStat(base, lv, IV, EV) + 5 + lv

def levelCalculator(Exp, group, maxLevel = 100):
    lv = 0
    required = 0
    while Exp >= required:
        lv += 1

        if group == "Fast":
            required = fast(lv)

        elif group == "Medium Fast":
            required = mediumFast(lv)

        elif group == "Medium Slow":
            required = mediumSlow(lv)

        elif group == "Slow":
            required = slow(lv)

        elif group == "Erratic":
            required = erratic(lv)

        elif group == "Fluctuating":
            required = fluctuating(lv)
        else:
            raise ValueError("ERROR: Unrecognized Experience Group")

        #level 100 is the maximum level for Pokemon
        if lv == maxLevel:
            break
    return lv

#Calculate the stats value as a function of EXP
def statsInExp(base, Exp, group, IV = 0, EV = 0, HP = False):
    if HP:
        return hpStat(base, levelCalculator(Exp, group), IV, EV)
    return otherStat(base, levelCalculator(Exp, group), IV, EV)

def getStatData(base, group = "Fast", IV = 0, EV = 0, minExp = 0, maxExp = 1250000, HP = False):
    exp = np.linspace(minExp, maxExp, 1000)
    val = []
    for xp in exp:
        val.append(statsInExp(base, xp, group, IV, EV, HP = HP))
    return exp, val

def plotStat(base, group = "Fast", IV = 0, EV = 0, minExp = 0, maxExp = 50000, HP = False):
    exp, val = getStatData(base, group, IV, EV, minExp, maxExp, HP)
    plt.plot(exp, val, label = "HP - " + str(HP))
    plt.legend()
    plt.xlabel("Experience")
    plt.ylabel("Stat Value")
    plt.show()
    return
"""
Compare the Stats of 2 pokemon, input the Base stat value you wish to compare and the Exp Groups.

"""
def compareBase(baseA, baseB, groupA, groupB, expMin = 0, expMax = 1250000, HPA = False, HPB = False):
    expA, valA = getStatData(baseA, groupA, HP = HPA, minExp = expMin, maxExp = expMax)
    expB, valB = getStatData(baseB, groupB, HP = HPB, minExp = expMin, maxExp = expMax)
    minLevel = min(levelCalculator(expMin, groupA),levelCalculator(expMin, groupB))
    maxLevel = max(levelCalculator(expMax, groupA),levelCalculator(expMax, groupB))
    plt.plot(expA, valA, label = "Pokemon A (" + str(levelCalculator(expMin, groupA)) + " - " + str(levelCalculator(expMax, groupA)) + ")")
    plt.plot(expB, valB, label = "Pokemon B (" + str(levelCalculator(expMin, groupB)) + " - " + str(levelCalculator(expMax, groupB)) + ")")
    plt.legend()
    plt.title("Min Lv. " + str(minLevel) + " - " + "Max Lv. " + str(maxLevel))
    plt.xlabel("Experience")
    plt.ylabel("Stat Value")
    plt.show()
    return
