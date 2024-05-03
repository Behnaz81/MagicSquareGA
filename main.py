###########################################################
###Project Title: MagicSquareGA
###Author: Behnaz Mohammad Hasani Zadeh
###Date: 4/28/2024
###Github Repository: https://github.com/Behnaz81/MagicSquareGA
###Description: This project will solve Magic Square problem
###using genetic algorithm.
############################################################

import random
import matplotlib.pyplot as plt

##The N##
SQUARE_SIZE = 3

##The Mutation Rate##
MUTATION_RATE = 0.05

##############Make The Primary Population#############

######This Function will make the primary population
######The genes will be made of random numbers and
######And no genes will be repeating in the population.
def makePrimaryPopulation(populationSize):
    numbers = list(range(1, SQUARE_SIZE ** 2 + 1))
    population = [random.sample(numbers, len(numbers)) for _ in range(populationSize)]

    return population



###################Make the Secondary Population#################

######This function uses TOURNAMENT selection method to choose
######from the primary population.
def makeSecondaryPopulation(primaryPopulation, populationSize):
    secondaryPopulation = []
    for i in range(populationSize):
        element1 = random.randint(0, len(primaryPopulation) - 1)
        element2 = random.randint(0, len(primaryPopulation) - 1)

        while element1 == element2:
            element2 = random.randint(0, len(primaryPopulation) - 1)

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
def crossover(secondaryPopulation):
    child1 = []
    child2 = []
    parent1 = secondaryPopulation[0]
    parent2 = secondaryPopulation[1]
    for i in range(SQUARE_SIZE):
        child1.append(parent1[i])
        child2.append(parent2[i])
    for i in range(SQUARE_SIZE * 3):
        if parent2[i] not in child1:
            child1.append(parent2[i])
        if parent1[i] not in child2:
            child2.append(parent1[i])

    return child1, child2



########################Mutation#########################

######This function will do the mutation. For each element
######a random number between 0 and 1 will be generated. If
######the random number was less than mutation rate the element
######swaps places with another random element.
def mutation(population):
    fitnesses = []
    for element in population:
        for i in range(0, len(element)):

            randomNumber = random.random()

            if randomNumber < MUTATION_RATE:
                indx = random.randint(0, len(element) - 1)
                while indx == i:
                    indx = random.randint(0, len(element) - 1)
                element[i], element[indx] = element[indx], element[i]
        fitnesses.append(fitness(element))

    return population, fitnesses


####################Fitness#######################

######This function calculates the fitness of a gene.
######It's based on how many rows, columns and diameters
######don't have the sum of 15. So the less the fitness is,
######the better the gene is.
def fitness(element):
    error = 0

    #For rows
    for j in range(SQUARE_SIZE):
        sum = 0
        for i in range(SQUARE_SIZE):
            sum += element[j * 3 + i]
        if sum != 15:
            error += 1

    #For columns
    for j in range(SQUARE_SIZE):
        sum = 0
        for i in range(SQUARE_SIZE):
            sum += element[j + i * 3]
        if sum != 15:
            error += 1

    #For diameter
    if (element[0] + element[4] + element[8]) != 15:
        error += 1

    if (element[3] + element[5] + element[7]) != 15:
        error += 1

    return error



#######################Print#######################
######This function helps us to print the genes.
def printElement(element):
    for i in range(SQUARE_SIZE):
        for j in range(SQUARE_SIZE):
            print(element[i * 3 + j], end="")
        print()



####################Main####################

fitnesses = []
bestFitnesses = []
#Make a population with 50 genes
population = makePrimaryPopulation(50)
#Save the fitnesses in a list
for i in range(50):
    fitnesses.append(fitness(population[i]))

# print("Primary population:")
#Printing the first population
# for element in population:
#     printElement(element)
#     print()

bestFitnesses.append(min(fitnesses))

#As long as the minimum fitness is 2 or more we continue making new genes
while(min(fitnesses) >= 2):

    #Choose two parents and make a secondary population
    secondaryPopulation = makeSecondaryPopulation(population, 2)

    # print("Secondary population:")
    # for element in secondaryPopulation:
    #     printElement(element)
    #     print()

    #Do the cross over
    child1, child2 = crossover(secondaryPopulation)

    # print("After Crossover:")
    # printElement(child1)
    # print()
    # printElement(child2)
    # print()

    #Add the new genes to the population
    population.append(child1)
    population.append(child2)

    #Mutate the whole population
    population, fitnesses = mutation(population)

    #Find the best fitness of this generation
    bestFitnesses.append(min(fitnesses))
    
    # print("After Mutation:")
    # for element in secondaryPopulation:
    #     printElement(element)
    #     print()


#The final solution!
print("Final Solution:")
printElement(population[fitnesses.index(min(fitnesses))])

#To show the best fitnesses we had in each generation
plt.scatter(list(range(len(bestFitnesses))), bestFitnesses)
plt.show()