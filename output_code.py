import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms

# Problem configuration
N_CITIES = 1000
POPULATION_SIZE = 100
GENERATIONS = 500
MUTATION_RATE = 0.01
CROSSOVER_RATE = 0.8
TOURNAMENT_SIZE = 5

# Create fitness type
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Generate distance matrix
np.random.seed(42)
distance_matrix = np.random.rand(N_CITIES, N_CITIES)
distance_matrix = (distance_matrix + distance_matrix.T) / 2

def evaluate(individual):
    """Calculate fitness based on tour distance (inverted for maximization)"""
    total_distance = 0.0
    for i in range(len(individual)):
        city_from = individual[i]
        city_to = individual[(i + 1) % len(individual)]
        total_distance += distance_matrix[city_from, city_to]
    fitness = 1.0 / (total_distance + 1e-10)
    return (fitness,)

def order_crossover(parent1, parent2):
    """Order-based crossover for TSP"""
    n_cities = len(parent1)
    child = np.zeros(n_cities, dtype=int)
    
    start = np.random.randint(0, n_cities)
    end = np.random.randint(start + 1, n_cities)
    
    child[start:end] = parent1[start:end]
    
    child_idx = end
    parent2_idx = end
    while child_idx < n_cities:
        if child_idx == end:
            child_idx = start
        child[child_idx] = parent2[parent2_idx]
        parent2_idx = (parent2_idx + 1) % n_cities
        child_idx = (child_idx + 1) % n_cities
    
    ind1 = creator.Individual(child) 
    ind2 = creator.Individual(parent2) # Crossover usually produces 2; simplified here
    return ind1, ind2

def swap_mutation(individual, mutation_rate=MUTATION_RATE):
    """Apply swap mutation to individual"""
    mutated = individual.copy()
    if np.random.random() < mutation_rate:
        n_cities = len(mutated)
        idx1, idx2 = np.random.choice(n_cities, size=2, replace=False)
        mutated[idx1], mutated[idx2] = mutated[idx2], mutated[idx1]
    return mutated

import numpy as np

def tournament_selection(individuals, k, tournament_size=TOURNAMENT_SIZE):
    """Select k individuals using tournament selection"""
    chosen = []
    for _ in range(k):
        # Select random indices for the tournament
        tournament_indices = np.random.choice(len(individuals), size=tournament_size, replace=False)
        
        # Extract fitness values from the DEAP individual objects
        # DEAP stores fitness in the .fitness.values attribute (usually a tuple)
        tournament_fitnesses = [individuals[i].fitness.values[0] for i in tournament_indices]
        
        # Identify the winner
        best_idx_in_tournament = np.argmax(tournament_fitnesses)
        chosen.append(individuals[tournament_indices[best_idx_in_tournament]])
        
    return chosen
def create_individual():
    """Generate a TSP individual as a permutation of N_CITIES indices"""
    genome = np.random.permutation(N_CITIES)
    return creator.Individual(genome.tolist())

def initialize_population(pop_size=POPULATION_SIZE):
    """Initialize population of TSP individuals"""
    population = [create_individual() for _ in range(pop_size)]
    return population

# Register toolbox operators
toolbox = base.Toolbox()
toolbox.register("individual", create_individual)
toolbox.register("population", tools.initRepeat, list, create_individual)
toolbox.register("mate", order_crossover)
toolbox.register("mutate", swap_mutation, mu=1, indpb=MUTATION_RATE)
toolbox.register("select", tournament_selection)
toolbox.register("evaluate", evaluate)

def evolutionary_loop(population, n_generations=GENERATIONS):
    """Main evolutionary algorithm loop"""
    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("avg", np.mean)
    stats.register("max", np.max)
    
    hof = tools.HallOfFame(1)
    
    algorithms.eaSimple(population, toolbox, cxpb=CROSSOVER_RATE, mutpb=MUTATION_RATE, 
                       ngen=n_generations, stats=stats, halloffame=hof, verbose=True)
    
    return hof[0], stats

def plot_tsp_tour(best_tour, city_coordinates):
    """Plot the TSP tour"""
    fig, ax = plt.subplots(figsize=(10, 10))
    
    n_cities = len(best_tour)
    ax.scatter(city_coordinates[:, 0], city_coordinates[:, 1], 
               c='blue', s=10, alpha=0.6, label='Cities')
    
    tour_x = city_coordinates[best_tour, 0]
    tour_y = city_coordinates[best_tour, 1]
    
    tour_x_closed = np.concatenate([tour_x, [tour_x[0]]])
    tour_y_closed = np.concatenate([tour_y, [tour_y[0]]])
    
    ax.plot(tour_x_closed, tour_y_closed, 
            color='red', linewidth=1.5, label='TSP Tour')
    
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_title('TSP Tour Visualization')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig, ax

if __name__ == "__main__":
    # Generate random city coordinates
    city_coordinates = np.random.rand(N_CITIES, 2) * 100
    
    # Initialize population
    population = initialize_population()
    
    # Run evolution
    best_individual, stats = evolutionary_loop(population)
    
    # Plot results
    fig, ax = plot_tsp_tour(best_individual, city_coordinates)
    plt.savefig("tsp_result.png", dpi=150)
    plt.close()
    
    print(f"Best fitness: {best_individual.fitness.values[0]:.6f}")
    print(f"Average fitness: {stats.values['avg']:.6f}")
    print(f"Max fitness: {stats.values['max']:.6f}")