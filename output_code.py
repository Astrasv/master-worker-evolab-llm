import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools

# Problem configuration
n = 10  # Number of cities
lower_bound = 0
upper_bound = 100

# Creator setup
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

# Evaluate function
def evaluate(individual):
    fitness = 0
    for i in range(len(individual) - 1):
        fitness += distances[individual[i]][individual[i+1]]
    fitness += distances[individual[-1]][individual[0]]
    return fitness,

def mate(parent1, parent2):
    crossover_point = np.random.randint(0, len(parent1))
    child1 = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
    child2 = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))
    return child1, child2

def mutate(individual):
    mutation_point1 = np.random.randint(0, len(individual))
    mutation_point2 = np.random.randint(0, len(individual))
    individual[mutation_point1], individual[mutation_point2] = individual[mutation_point2], individual[mutation_point1]
    return individual

def select(population, fitness):
    parents = np.random.choice(population, size=2, p=fitness/np.sum(fitness))
    return parents

def create_individual(n):
    genome = np.random.permutation(n)
    return genome

def initialize_population(n, population_size):
    population = []
    for _ in range(population_size):
        individual = create_individual(n)
        population.append(individual)
    return population

def run_evolutionary_loop(population, fitness_function, num_generations):
    for generation in range(num_generations):
        population = select(population, fitness_function)
        population = mate(population)
        population = mutate(population)
    return population

def visualize_results(results):
    plt.figure(figsize=(8, 6))
    plt.plot(results['distance'], label='Distance')
    plt.xlabel('Iteration')
    plt.ylabel('Distance')
    plt.title('Travelling Salesman Problem Results')
    plt.legend()
    plt.show()

distances = np.random.randint(lower_bound, upper_bound, size=(n, n))

toolbox = base.Toolbox()
toolbox.register("individual", create_individual, n=n)
toolbox.register("population", initialize_population, n=n, population_size=100)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", mate)
toolbox.register("mutate", mutate)
toolbox.register("select", select)

population = toolbox.population()
fitness_function = toolbox.evaluate
num_generations = 100

results = run_evolutionary_loop(population, fitness_function, num_generations)
visualize_results(results)