
# Cell 0: imports
import numpy as np
import random
from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import matplotlib.pyplot as plt

# Cell 1: problem configuration
NUM_CITIES = 10
POPULATION_SIZE = 100
NUM_GENERATIONS = 100
MUTATION_RATE = 0.01

# Cell 2: creator setup
creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
creator.create('Individual', list, fitness=creator.FitnessMin)

# Cell 3: evaluate function
def evaluate(individual, distances):
    distance = 0
    for i in range(len(individual) - 1):
        distance += distances[individual[i], individual[i + 1]]
    distance += distances[individual[-1], individual[0]]
    return distance,

# Cell 4: mate/crossover function
def ordered_crossover(parent1, parent2):
    child = np.zeros_like(parent1)
    start_idx = np.random.randint(0, len(parent1))
    end_idx = np.random.randint(start_idx + 1, len(parent1) + 1)
    child[start_idx:end_idx] = parent1[start_idx:end_idx]
    index = 0
    for i in range(len(parent2)):
        if parent2[i] not in child:
            while child[index] != 0:
                index += 1
            child[index] = parent2[i]
    return child

# Cell 5: mutation function
def mutate(individual):
    if np.random.rand() < MUTATION_RATE:
        i, j = np.random.randint(0, len(individual), size=2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual

# Cell 6: selection function
def select_parents(population, fitness, num_parents):
    sorted_indices = np.argsort(fitness)
    selected_indices = sorted_indices[:num_parents]
    selected_parents = [population[i] for i in selected_indices]
    return selected_parents

# Cell 7: additional operators
def initialize_population(population_size, num_cities):
    population = [np.random.permutation(num_cities) for _ in range(population_size)]
    return population

# Cell 8: initialization functions
def create_individual(num_cities):
    genome = np.random.permutation(num_cities)
    return genome

# Cell 9: toolbox registration
toolbox = base.Toolbox()
toolbox.register('individual', create_individual, NUM_CITIES)
toolbox.register('population', tools.initRepeat, list, toolbox.individual)
toolbox.register('evaluate', evaluate, distances=np.random.rand(NUM_CITIES, NUM_CITIES))
toolbox.register('mate', ordered_crossover)
toolbox.register('mutate', mutate)
toolbox.register('select', tools.selTournament, tournsize=3)

# Cell 10: main evolution loop
def evolutionary_loop(population_size, num_cities, num_generations, mutation_rate):
    population = toolbox.population(n=population_size)
    for _ in range(num_generations):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=mutation_rate)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population))
    return population

# Cell 11: results, plotting, statistics
def plot_results(population):
    distances = np.random.rand(NUM_CITIES, NUM_CITIES)
    fitness = [evaluate(individual, distances)[0] for individual in population]
    plt.plot(fitness)
    plt.show()

population = evolutionary_loop(POPULATION_SIZE, NUM_CITIES, NUM_GENERATIONS, MUTATION_RATE)
plot_results(population)
