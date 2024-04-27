import random
import numpy as np

##The N##
SQUARE_SIZE = 3

##############Make The Primary Population#############

######This Function will make the primary population
######The genes will be made of random numbers and
######And no genes will be repeating in the population.
def makePrimaryPopulation(populationSize):
    numbers = list(range(1, 10))
    population = [random.sample(numbers, len(numbers)) for _ in range(populationSize)]

    return population



###################Make the Secondary Population#################

######This function uses TOURNAMENT selection method to choose
######from the primary population.
def makeSecondaryPopulation(primaryPopulation, populationSize):
    secondaryPopulation = []
    for i in range(populationSize):
        element1 = random.randint(0, 9)
        element2 = random.randint(0, 9)

        while element1 != element2:
            element2 = random.randint(0, 9)

        if fitness(primaryPopulation[element1]) > fitness(primaryPopulation[element2]):
            secondaryPopulation.append(population[element1])
        else:
            secondaryPopulation.append(population[element2])

    return secondaryPopulation



#################Crossover#############################

######This function helps us to make new genes
######To pretend repeating elements we used this method:
######The first 3 elements come from one parent
######The rest are from the elements we haven't used from
######the other parent
def crossover(parent1, parent2):
    child1 = []
    child2 = []
    for i in range(SQUARE_SIZE):
        child1.append(parent1[i])
        child2.append(parent2[i])
    for i in range(SQUARE_SIZE * 3):
        if parent2[i] not in child1:
            child1.append(parent2[i])
        if parent1[i] not in child2:
            child2.append(parent1[i])

    return child1, child2



######This function makes a new population using crossover
######Between parents and children the one with the lowest
######fitness is in the new population.
def populationAfterCrossover(population):
    newPopulation = []

    for i in range(len(population)):
        for j in range(i + 1, len(population)):
            child1, child2 = crossover(population[i], population[j])

            child1Fitness = fitness(child1)
            child2Fitness = fitness(child2)
            parent1Fitness = fitness(population[i])
            parent2Fitness = fitness(population[j])

            # print("Child1:")
            # printElement(child1)
            # print("fitness: ", child1Fitness)
            # print("Child2:")
            # printElement(child2)
            # print("fitness: ", child2Fitness)
            # print("parent1:")
            # printElement(population[i])
            # print("fitness: ", parent1Fitness)
            # print("parent2:")
            # printElement(population[j])
            # print("fitness: ", parent2Fitness)



            if parent1Fitness < parent2Fitness:
                if parent1Fitness < child1Fitness:
                    if parent1Fitness < child2Fitness:
                        newPopulation.append(population[i])
                    else:
                        newPopulation.append(child2)
                else:
                    if child1Fitness < child2Fitness:
                        newPopulation.append(child1)
                    else:
                        newPopulation.append(child2)
            else:
                if parent2Fitness < child1Fitness:
                    if parent2Fitness < child2Fitness:
                        newPopulation.append(population[j])
                    else:
                        newPopulation.append(child2)
                else:
                    if child1Fitness < child2Fitness:
                        newPopulation.append(child1)
                    else:
                        newPopulation.append(child2)

    return newPopulation


def mutation(element):
    x1 = random.randint(0, 2)
    y1 = random.randint(0, 2)

    x2 = random.randint(0, 2)
    y2 = random.randint(0, 2)

    # print("Before:")
    # printElement(element)

    element[y1 + x1 * SQUARE_SIZE], element[y2 + x2 * SQUARE_SIZE] = element[y2 + x2 * SQUARE_SIZE], element[y1 + x1 * SQUARE_SIZE]

    # print("After:")
    # printElement(element)

    return element


def populationAfterMutation(population):
    newPopulation = []
    for i in range(len(population)):
        newGene = mutation(population[i])

        if fitness(newGene) < fitness(population[i]):
            newPopulation.append(newGene)
        else:
            newPopulation.append(population[i])

    return newPopulation


def fitness(element):
    error = 0

    for j in range(SQUARE_SIZE):
        sum = 0
        for i in range(SQUARE_SIZE):
            sum += element[j * 3 + i]
        if sum != 15:
            error += 1

    for j in range(SQUARE_SIZE):
        sum = 0
        for i in range(SQUARE_SIZE):
            sum += element[j + i * 3]
        if sum != 15:
            error += 1


    if (element[0] + element[4] + element[8]) != 15:
        error += 1

    if (element[3] + element[5] + element[7]) != 15:
        error += 1

    return error


def printElement(element):
    for i in element:
        print(i, end="")

#
# element = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# scoreElement = fitness(element)
#
# generation = 0
#
# print(("=" * 30) + " fitness: " + str(scoreElement) + " generation " + str(generation))
# print("")
# printElement(element)
#
# while (fitness(element) != 0):
#     mutant = mutation(element)
#     mutant = mutation(mutant)
#
#     score = fitness(mutant)
#
#     if (score < scoreElement):
#         scoreElement = score
#         element = mutant
#
#     generation += 1
#     print(("=" * 30) + " fitness: " + str(scoreElement) + " generation " + str(generation))
#     print("")
#     printElement(element)


population = []
#Make a population with 10 genes
population = makePrimaryPopulation(10)
print("Primary population:")
#Printing the first population
for element in population:
    printElement(element)
    print()

secondaryPopulation = makeSecondaryPopulation(population, 2)
print("Secondary population:")
for element in secondaryPopulation:
    printElement(element)
    print()

# newPopulation = []
#
# newPopulation = populationAfterCrossover(population)
# print("New Population:")
# for element in newPopulation:
#     printElement(element)
#     print()

# newPopulation = populationAfterMutation(newPopulation)
# print("New Population:")
# for element in newPopulation:
#     printElement(element)
#     print()
#     print("fitness:", fitness(element))
#     print()