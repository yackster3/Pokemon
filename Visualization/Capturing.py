import numpy as np
from matplotlib import pyplot as plt
import math

"""
    returns the modified Catch Rate of the Pokemon
"""
def modifiedRate(maxHP, curHP, rate, ballBonus, status):
    statusBonus = 1
    if status == "freeze" or status == "sleep":
        statusBonus = 2
    elif status == "paralyze" or status == "burn" or status == "poison":
        statusBonus = 1.5

    modRate = (3*maxHP-2*curHP)*rate*ballBonus*statusBonus/(3*maxHP)
    return modRate
"""
    returns the balls catchRate
"""
def ballBonus(ball, myLv = 1, catchLv = 1, moon = False, fishing = False,
    genderDif = False, speciesDif = False, weight = 0, baseSpeed = 0,
    type = None, caught = False, inWater = False, turnCount = 0):
    if ball == "Poke" or ball == "Friend" or ball == "Heal" or ball == "Cherish" or ball == "Premier" or ball == "Luxury":
        return 1
    elif ball == "Great" or ball == "Safari" or ball == "Sport":
        return 1.5
    elif ball == "Ultra":
        return 2
    elif ball == "Master":
        return 99999999999999
    elif ball == "Level":
        if myLv <= catchLv:
            return 1
        elif myLv //catchLv <2:
            return 2
        elif myLv //catchLv<4:
            return 4
        else:
            return 8
    elif ball == "Moon":
        if moon:
            return 4
        else:
            return 1
    elif ball == "Love":
        if gender and not species:
            return 8
    elif ball == "Heavy":
        if weight < 225.8:
            return -20
        elif weight < 451.5:
            return 1
        elif weight < 677.3:
            return 20
        elif weight < 903:
            return 30
        else:
            return 40
    elif ball == "Fast":
        if baseSpeed >= 100:
            return 4
        else:
            return 1
    elif ball == "Net":
        if "Water" in type or "Bug" in type:
            return 3
        else:
            return 1
    elif ball == "Nest":
        if catchLv < 30:
            return (40-catchLv)/10
        else:
            return 1
    elif ball == "Repeat":
        if caught:
            return 3
        else:
            return 1
    elif ball == "Timer":
        multi = (turnCount+10)/10
        if multi >= 4:
            return 4
        else:
            return multi
    elif ball == "Dive":
        if inWater:
            return 3.5
        else:
            return 1
    elif ball == "Dusk":
        if dark:
            return 3.5
        else:
            return 1
    elif ball == "Quick":
        if turnCount == 0:
            return 4
        else:
            return 1
    elif ball == "Beast":
        if beast:
            return 5
        else:
            return .1
    else:
        raise ValueError("Ball Type not found, please input valid ball type (don't include 'ball')")
    raise ValueError("Unexpected end reached (You put this message here dipstick)")
    return

"""
    a is the modifiedRate
    returns the number of successful shakes, 4 shakes implies successful capture
"""
def ShakeChecks(a):
    if a > 255:
        return 4
    b = 1048569/np.sqrt(np.sqrt(16711680/a))
    count = 0
    for i in range(4):
        rand = np.random.randint(0, 65535)
        if rand < b:
            count += 1
    return count

def testShakes():
    a = modifiedRate(100, 10, 3, ballBonus("Ultra"), "sleep")
    return ShakeChecks(a)
"""
    runs simulations on ez ball calculations
"""
def EZsimulations(ball = "Ultra", hpMax = 100, hpCur = 10, pokeRate = 3, status = "sleep", N = 10000):
    attemptsToCapture = []
    p = 0
    totalRoll = 0
    a = modifiedRate(hpMax, hpCur, pokeRate, ballBonus(ball), status)

    for i in range(N):
        counter = 1
        p+=1
        totalRoll += 1
        while ShakeChecks(a) < 4:
            counter += 1
            totalRoll += 1
        attemptsToCapture.append(counter)

    mean, var = sum(attemptsToCapture)/N, np.var(attemptsToCapture)
    r = 1
    p = p/totalRoll
    maxVal = max(attemptsToCapture)
    x = []
    y = []
    for i in range(0, maxVal):
        x.append(i)
        y.append(negativeBinomialDist(i, p, r))

    plt.plot(x, y, label = "probability: " + str(round(100*p, 3)) + "%")
    plt.hist(attemptsToCapture, bins = maxVal, normed = True, label = "Data")
    plt.legend()
    plt.xlabel("Attempts")
    plt.ylabel("Success Counts")
    plt.title("Distribution for " + ball + " Ball " + status  + ", Catch Rate: " + str(pokeRate) + ", HP: " + str(round(hpCur*100/hpMax)) + "%")
    plt.show()

    return sum(attemptsToCapture)/N, np.var(attemptsToCapture)

"""
    Compares balls that are simple to calculate effectiveness.
"""
def EZCompareBalls(ballA = "Poke", ballB = "Ultra", hpMax = 100, hpCur = 10, pokeRate = 3, status = "sleep", N = 10000):
        attemptsToCapturea = []
        attemptsToCaptureb = []

        pa = 0
        pb = 0

        totalRolla = 0
        totalRollb = 0

        a1 = modifiedRate(hpMax, hpCur, pokeRate, ballBonus(ballA), status)
        a2 = modifiedRate(hpMax, hpCur, pokeRate, ballBonus(ballB), status)

        for i in range(N):
            countera = 1
            counterb = 1

            pb+=1
            pa+=1

            totalRolla += 1
            totalRollb += 1

            while ShakeChecks(a1) < 4:
                countera += 1
                totalRolla += 1

            while ShakeChecks(a2)<4:
                counterb += 1
                totalRollb += 1

            attemptsToCapturea.append(countera)
            attemptsToCaptureb.append(counterb)

        meana, vara = sum(attemptsToCapturea)/N, np.var(attemptsToCapturea)
        meanb, varb = sum(attemptsToCaptureb)/N, np.var(attemptsToCaptureb)

        r = 1

        pa = pa/totalRolla
        pb = pb/totalRollb

        maxVala = max(attemptsToCapturea)
        maxValb = max(attemptsToCaptureb)

        xa = []
        ya = []

        xb = []
        yb = []

        for i in range(0, maxVala):
            xa.append(i)
            ya.append(negativeBinomialDist(i, pa, r))

            xb.append(i)
            yb.append(negativeBinomialDist(i, pb, r))

        plt.plot(xa, ya, label = str(ballA) + " Probability: " + str(round(100*pa, 3)) + "%")
        plt.plot(xb, yb, label = str(ballB) + " Probability: " + str(round(100*pb, 3)) + "%")
        plt.hist(attemptsToCapturea, bins = max(maxVala, maxValb), normed = True, label = "Data for " + str(ballA))
        plt.hist(attemptsToCaptureb, bins = max(maxVala, maxValb), normed = True, label = "Data for " + str(ballB))

        plt.legend()
        plt.xlabel("Attempts")
        plt.ylabel("Success Counts")
        plt.title("Compare " + str(ballA) + " with " + str(ballB))
        plt.show()
"""
    Compare the pokeball distributions and how long to catch for various pokeballs. This function assumes the wild
    pokemon is in the same state throughout the battle but does take in to account turn count.
"""
def ComplexCompareBalls(ballA = "Quick", ballB = "Timer", hpMax = 100, hpCur = 10, pokeRate = 3, status = "sleep", N = 10000,
                    myLv = 1, catchLv = 1, moon = False, fishing = False, genderDif = False, speciesDif = False,
                    weight = 0, baseSpeed = 0, type = None, caught = False, inWater = False, turnCountStart = 1):
        attemptsToCapturea = []
        attemptsToCaptureb = []

        pa = 0
        pb = 0

        totalRolla = 0
        totalRollb = 0

        for i in range(N):
            turnCount = turnCountStart
            bonusA = ballBonus(ballA, myLv, catchLv, moon, fishing, genderDif, speciesDif, weight, baseSpeed, type, caught, inWater, turnCount)
            bonusB = ballBonus(ballB, myLv, catchLv, moon, fishing, genderDif, speciesDif, weight, baseSpeed, type, caught, inWater, turnCount)

            a1 = modifiedRate(hpMax, hpCur, pokeRate, bonusA, status)
            a2 = modifiedRate(hpMax, hpCur, pokeRate, bonusB, status)

            countera = 1
            counterb = 1

            pb+=1
            pa+=1

            totalRolla += 1
            totalRollb += 1

            while ShakeChecks(a1) < 4:
                countera += 1
                totalRolla += 1
                turnCount += 1

            turnCount = turnCountStart
            while ShakeChecks(a2)<4:
                counterb += 1
                totalRollb += 1
                turnCount += 1
            attemptsToCapturea.append(countera)
            attemptsToCaptureb.append(counterb)

        meana, vara = sum(attemptsToCapturea)/N, np.var(attemptsToCapturea)
        meanb, varb = sum(attemptsToCaptureb)/N, np.var(attemptsToCaptureb)

        r = 1

        pa = pa/totalRolla
        pb = pb/totalRollb

        maxVala = max(attemptsToCapturea)
        maxValb = max(attemptsToCaptureb)

        xa = []
        ya = []

        xb = []
        yb = []

        for i in range(0, maxVala):
            xa.append(i)
            ya.append(negativeBinomialDist(i, pa, r))

            xb.append(i)
            yb.append(negativeBinomialDist(i, pb, r))

        plt.plot(xa, ya, label = str(ballA) + " Probability: " + str(round(100*pa, 3)) + "%")
        plt.plot(xb, yb, label = str(ballB) + " Probability: " + str(round(100*pb, 3)) + "%")
        plt.hist(attemptsToCapturea, bins = max(maxVala, maxValb), normed = True, label = "Data for " + str(ballA))
        plt.hist(attemptsToCaptureb, bins = max(maxVala, maxValb), normed = True, label = "Data for " + str(ballB))
        print(attemptsToCapturea[0])
        print(attemptsToCaptureb[0])
        plt.legend()
        plt.xlabel("Attempts")
        plt.ylabel("Success Counts")
        plt.title("Compare " + str(ballA) + " with " + str(ballB))
        plt.show()

"""
    This plots a Negative Binomial Distribution...which is useful here for
    determining the probability of catching a pokemon within x attempts.
"""
def negativeBinomialDist(x, p, r = 1):
    def comb(i, j):
        i = int(i)
        j = int(j)
        return math.factorial(i)/(math.factorial(j)*(math.factorial(i-j)))
    return comb((x+r-1), x)*(1-p)**x*(p**r)
