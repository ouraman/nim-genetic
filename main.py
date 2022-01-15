#!/usr/bin/env python3

# learning nim with a genetic algorithm



#------------------------------------------------------------------------------
# IMPORTS

import random

#------------------------------------------------------------------------------
# PARAMETERS

PILE_SIZE = 100

INDIV_POSITIONS = 50
INDIV_STEPS = [1,3,4]

INIT_POP_SIZE = 100
MAX_POP_SIZE = 1000

MUTATION_PROB = 0.02
MUTATION_PRCT = 0.05

population = []

#------------------------------------------------------------------------------
# SUBROUTINES

def init():
    for i in range(INIT_POP_SIZE):
        individual = []
        for j in range(INDIV_POSITIONS):
            probsum = 0
            probdict = {}
            for step in INDIV_STEPS[:-1]:
                prob = random.uniform(0,1-probsum)
                probsum = probsum + prob
                probdict[step] = prob
            probdict[INDIV_STEPS[-1]] = 1-probsum
            individual.append(probdict)
        population.append(individual)


def play(indiv1, indiv2, pile_size):
    p_size = pile_size
    indivs = [indiv1, indiv2]
    random.shuffle(indivs)
    count = 0
    while p_size != 0:
        rr = random.random()
        step_size = 0
        probsum = 0
        for step in indivs[count%2][p_size%INDIV_POSITIONS]:
            if probsum < rr and rr <= probsum+indivs[count%2][p_size%INDIV_POSITIONS][step]:
                step_size = step
                break
            probsum = probsum + indivs[count%2][p_size%INDIV_POSITIONS][step]

        if p_size - step_size == 0:
            return indivs[count%2]
        elif p_size - step_size > 0:
            p_size = p_size - step_size

        count = count + 1


def progress():
    global population

    if len(population)%2 != 0:
        population.append(random.choice(population))

    random.shuffle(population)

    winners = []
    for i in range(int(len(population)/2)):
        winners.append(play(population[i],population[-i-1],PILE_SIZE))

    population = winners

    winners2 = winners.copy()

    random.shuffle(winners)
    random.shuffle(winners2)

    children = []
    for w1, w2 in zip(winners,winners2):
        child = []
        for pos1, pos2 in zip(w1,w2):
            probs = {}
            for step in INDIV_STEPS:
                probs[step] = (pos1[step]+pos2[step])/2.0
            child.append(probs)
        children.append(child)

    population.extend(children)

    for child in children:
        for pos in child:
            if random.random() < MUTATION_PROB:
                idx = INDIV_STEPS.copy()
                cc = random.choice(idx)
                idx.remove(cc)
                if random.random() < 0.5:
                    pos[cc] += MUTATION_PRCT*(1-pos[cc])
                else:
                    pos[cc] -= MUTATION_PRCT*pos[cc]

                cc = random.choice(idx)
                idx = INDIV_STEPS.copy()
                idx.remove(cc)
                psum = 0
                for ii in idx:
                    psum += pos[ii]

                pos[cc] = 1-psum

    population.extend(children)


def purge():
    global population

    if len(population)%2 != 0:
        population.append(random.choice(population))

    random.shuffle(population)

    winners = []
    for i in range(int(len(population)/2)):
        winners.append(play(population[i],population[-i-1],PILE_SIZE))

    population = winners

#------------------------------------------------------------------------------
# MAIN

def main():
    init()

    for i in range(5000):
        print(i)
        progress()
        if len(population) > MAX_POP_SIZE:
            purge()

    print(len(population))

    print(population[0][1])
    print(population[0][2])
    print(population[0][3])
    print(population[0][4])

    print(population[-1][1])
    print(population[-1][2])
    print(population[-1][3])
    print(population[-1][4])

#------------------------------------------------------------------------------
# RUN

if __name__ == "__main__":
    main()
