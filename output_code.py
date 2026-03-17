import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools

# Problem configuration
n = 10
population_size = 100
num_generations = 100
mutation_rate = 0.1

def define_travelling_salesman_problem(n):
    # Define the problem
    cities = np.arange(n)
    distances = np.random.rand(n, n)
    return cities, distances

def create_individual(n):
    genome = np.random.permutation(n)
    return genome

def initialize_population(n, population_size):
    population = []
    for _ in range(population_size):
        genome = create_individual(n)
        population.append(genome)
    return population

def fitness_function(genome):
    total_distance = 0
    n = len(genome)
    for i in range(n):
        city1 = genome[i]
        city2 = genome[(i + 1) % n]
        distance = calculate_distance(city1, city2)
        total_distance += distance
    return 1 / total_distance

def select_parents(population, fitness):
    # Select parents based on fitness
    parents = np.random.choice(population, size=len(population), p=fitness/np.sum(fitness))
    return parents

def crossover(parent1, parent2):
    crossover_point = np.random.randint(1, len(parent1))
    child = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
    return child

def mutate(individual):
    mutation_point = np.random.randint(len(individual))
    individual[mutation_point] = np.random.randint(len(individual))
    return individual

def evolutionary_loop(population, fitness_function, mutation_rate, num_generations):
    for generation in range(num_generations):
        parents = select_parents(population, fitness_function)
        offspring = crossover(parents)
        offspring = mutate(offspring, mutation_rate)
        population = offspring
    best_individual = select_best_individual(population, fitness_function)
    return best_individual

def visualize_results(route, cities):
    x = [city[0] for city in cities]
    y = [city[1] for city in cities]

    plt.figure(figsize=(8, 6))
    plt.plot(x, y, 'bo-')
    plt.plot(x + [x[0]], y + [y[0]], 'r-')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Travelling Salesman Problem Route')
    plt.show()

# Toolbox registration
creator.create('FitnessMax', base.Fitness, weights=(1.0,))
creator.create('Individual', list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register('individual', create_individual)
toolbox.register('population', initialize_population)
toolbox.register('evaluate', fitness_function)
toolbox.register('mate', crossover)
toolbox.register('mutate', mutate)
toolbox.register('select', tools.selTournament, tournsize=3)

def main():
    cities, distances = define_travelling_salesman_problem(n)
    population = toolbox.population(n, population_size)
    fitness = toolbox.map(toolbox.evaluate, population)
    population = toolbox.select(population, fitness)
    best_individual = evolutionary_loop(population, fitness_function, mutation_rate, num_generations)
    visualize_results(best_individual, cities)

if __name__ == '__main__':
    main()