###########################################################
###Project Title: MagicSquareGA
###Author: Behnaz Mohammad Hasani Zadeh
###Date: 4/28/2024
###Description: This project will solve Magic Square problem
###using genetic algorithm.
############################################################

import random
import matplotlib.pyplot as plt

##The N##
SQUARE_SIZE = 9

##Primaty Population Size##
PRIMARY_POPULATION_SIZE = 1000

##The Mutation Rate##
MUTATION_RATE = 0.03

##The Cross Over Rate##
CROSSOVER_RATE = 0.8

##The T Tournament Selection##
T = 2


#######################Print#######################

######This function helps us to print the genes.
def printElement(element):
    for i in range(SQUARE_SIZE):
        for j in range(SQUARE_SIZE):
            print(element[i * 9 + j], end=" ")
        print()



####################Fitness#######################

######This function calculates the fitness of a gene.
######It's based on how many rows, columns and diameters
######don't have the sum we want. So the less the fitness is,
######the better the gene is.
def fitness(element):


    error = 0

    #For rows
    for j in range(SQUARE_SIZE):
        sum = 0
        for i in range(SQUARE_SIZE):
            sum += element[j * 9 + i]
        if sum != SQUARE_SIZE * (SQUARE_SIZE ** 2 + 1) / 2:
            error += 1

    #For columns
    for j in range(SQUARE_SIZE):
        sum = 0
        for i in range(SQUARE_SIZE):
            sum += element[j + i * 9]
        if sum != SQUARE_SIZE * (SQUARE_SIZE ** 2 + 1) / 2:
            error += 1

    #For diameter
    if (element[0] + element[10] + element[19] + element[30]+ element[40] + element[50] + element[60] + element[70] + element[80]) != SQUARE_SIZE * (SQUARE_SIZE ** 2 + 1) / 2:
        error += 1

    if (element[8] + element[16] + element[24] + element[32] + element[40] + element[48] + element[56] + element[63] + element[72]) != SQUARE_SIZE * (SQUARE_SIZE ** 2 + 1) / 2:
        error += 1

    return error



##############Make The Primary Population#############

######This Function will make the primary population
######The genes will be made of random numbers and
######And no genes will be repeating in the population.
def makePrimaryPopulation(populationSize):
    numbers = list(range(1, SQUARE_SIZE ** 2 + 1))
    population = [random.sample(numbers, len(numbers)) for _ in range(populationSize)]

    return population



###############################Selection############################

######This function uses TOURNAMENT selection method to choose
######from the primary population.
def selection(primaryPopulation, populationSize):
    secondaryPopulation = []
    secondaryFitnesses = []

    while len(secondaryPopulation) < populationSize:
        elements = []
        fitnesses = []

        for i in range(T):
            randomNumber = random.randint(0, len(primaryPopulation) - 1)

            while primaryPopulation[randomNumber] in elements:
                randomNumber = random.randint(0, len(primaryPopulation) - 1)

            elements.append(primaryPopulation[randomNumber])
            fitnesses.append(fitness(primaryPopulation[randomNumber]))

        if elements[fitnesses.index(min(fitnesses))] not in secondaryPopulation:
            secondaryPopulation.append(elements[fitnesses.index(min(fitnesses))])
            secondaryFitnesses.append(min(fitnesses))

    return secondaryPopulation, secondaryFitnesses


#################Crossover#############################

######This function helps us to make new genes
######First a random point is chosen.
######Then the first part of the child will be
######from the one parent. Other elements are
######from the non-repeated elements from the
######other parent.
def crossover(parent1, parent2):
    child1 = []
    child2 = []
    randomPoint = random.randint(0, len(parent1) - 2)

    for i in range(randomPoint):
        child1.append(parent1[i])
        child2.append(parent2[i])

    for i in range(SQUARE_SIZE ** 2):
        if parent2[i] not in child1:
            child1.append(parent2[i])
        if parent1[i] not in child2:
            child2.append(parent1[i])

    return child1, child2



########################Mutation#########################

######This function will do the mutation. For the element
######a random number between 0 and 1 will be generated. If
######the random number was less than mutation rate two
######random elements will swap places.
def mutation(element):

    randomNumber = random.random()

    if randomNumber < MUTATION_RATE:
        element1 = random.randint(0, len(element) - 1)
        element2 = random.randint(0, len(element) - 1)
        while element1 == element2:
           element2 = random.randint(0, len(element) - 1)
        element[element1], element[element2] = element[element2], element[element1]

    return element



####################Main####################

fitnesses = []
bestFitnesses = []

#Make a primary population
population = makePrimaryPopulation(PRIMARY_POPULATION_SIZE)

#Save the fitnesses in a list
for i in range(PRIMARY_POPULATION_SIZE):
    fitnesses.append(fitness(population[i]))

bestFitnesses.append(min(fitnesses))
generation = 0

print(generation, bestFitnesses[generation])

#As long as the minimum fitness is 2 or more we continue making new genes
while(min(fitnesses) > 2):
    fitnesses = []

    #Choose parents and make a secondary population
    secondaryPopulation, secondaryFitnesses = selection(population, int(PRIMARY_POPULATION_SIZE * CROSSOVER_RATE))

    #Do the cross over for each two element from the secondary population
    length = len(secondaryPopulation)
    for i in range(0, length, 2):
        child1, child2 = crossover(secondaryPopulation[i], secondaryPopulation[i + 1])
        if child1 not in secondaryPopulation:
            secondaryPopulation.append(child1)
            secondaryFitnesses.append(fitness(child1))
        if child2 not in secondaryPopulation:
            secondaryPopulation.append(child2)
            secondaryFitnesses.append(fitness(child2))

    #Do the mutation for each element of the secondary population
    for i in range(len(secondaryPopulation)):
        afterMutation = mutation(secondaryPopulation[i])
        if afterMutation != secondaryPopulation[i]:
            secondaryPopulation.append(afterMutation)
            secondaryFitnesses.append(fitness(afterMutation))

    #Add the secondary population to the primary population
    for i in range(len(secondaryPopulation)):
        if secondaryPopulation[i] not in population:
            population.append(secondaryPopulation[i])
            fitnesses.append(secondaryFitnesses[i])

    #Choose from the new population using selection function
    population, fitnesses = selection(population, PRIMARY_POPULATION_SIZE)

    #Find the best fitness of this generation
    bestFitnesses.append(min(fitnesses))
    generation += 1
    print(generation, bestFitnesses[generation], len(population))

#The final solution!
print("Final Solution:")
printElement(population[fitnesses.index(min(fitnesses))])

#To show the best fitnesses we had in each generation
plt.plot(list(range(len(bestFitnesses))), bestFitnesses)
plt.xlabel("Generations")
plt.ylabel("Best Fitness")
plt.title("Fitness vs Generations")
plt.show()