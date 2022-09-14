import random
import math


def objective_function(vector):
    return sum([x**2 for x in vector])


def random_within_bounds(lower_bound, upper_bound):
    return lower_bound + (upper_bound-lower_bound) * random.random()


def generate_random_vector(search_space):
    return [random_within_bounds(lower_bound, upper_bound) for lower_bound, upper_bound in search_space]


def random_gaussian(mean=0.0, std=1.0):
    u1 = u2 = w = 0

    while True:
        u1 = 2 * random.random() - 1
        u2 = 2 * random.random() - 1
        w = u1 ** 2 + u2 ** 2
        if w < 1:
            break

    w = math.sqrt((-2 * math.log(w)) / w)

    return mean + (u2 * w) * std


def make_clone(parent):
    v = [parent['vector'][i] for i in range(len(parent['vector']))]
    return {'vector': v}


def calculate_mutation_rate(beta, normalized_cost):
    return (1 / beta) * math.exp(-normalized_cost)


def mutate(beta, child, normalized_cost):
    for i, x in enumerate(child['vector']):
        alpha = calculate_mutation_rate(beta, normalized_cost)
        child['vector'][i] = x + alpha * random_gaussian()


def clone_cell(beta, number_of_clones, parent):
    clones = [make_clone(parent) for _ in range(number_of_clones)]
    for clone in clones:
        mutate(beta, clone, parent['norm_cost'])
        clone['cost'] = objective_function(clone['vector'])
    clones = sorted(clones, key=lambda x: x['cost'])
    return clones[0]


def calculate_normalized_cost(population):
    population = sorted(population, key=lambda x: x['cost'])
    range = population[-1]['cost'] - population[0]['cost']
    if range == 0:
        for cell in population:
            cell['norm_cost'] = 1
    else:
        for cell in population:
            cell['norm_cost'] = 1 - (cell['cost'] / range)


def average_cost(population):
    sum = 0
    for cell in population:
        sum += cell['cost']
    return sum / len(population)


def get_euclidean_distance(city_from, city_to):
    return math.sqrt((city_from[0] - city_to[0])**2 + (city_from[1] - city_to[1])**2)


def get_neighbors(cell, population, affinity_threashold):
    neighbors = []
    for cell in population:
        if get_euclidean_distance(cell['vector'], cell['vector']) < affinity_threashold:
            neighbors.append(cell)
    return neighbors


def affinity_supress(population, affinity_threashold):
    population = []
    for cell in population:
        neighbors = get_neighbors(cell, population, affinity_threashold)
        neighbors = sorted(neighbors, key=lambda x: x['cost'])
        if len(neighbors) == 0 or cell == neighbors[0]:
            population.append(cell)
    return population


def search(search_space, max_gens, initial_population_size, number_of_clones, beta, number_of_random_cells_to_create, affinity_threashold):
    population = [{'vector': generate_random_vector(
        search_space)} for _ in range(initial_population_size)]
    best = None
    for _ in range(max_gens):
        for cell in population:
            cell['cost'] = objective_function(cell['vector'])
        calculate_normalized_cost(population)
        population = sorted(population, key=lambda x: x['cost'])
        if best is None or population[0]['cost'] < best['cost']:
            best = population[0]
        avg_Cost = average_cost(population)
        while True:
            progeny = [clone_cell(beta, number_of_clones, population[i])
                       for i in range(len(population))]
            if average_cost(progeny) < avg_Cost:
                break

        population = affinity_supress(progeny, affinity_threashold)
        for _ in range(number_of_random_cells_to_create):
            population.append({'vector': generate_random_vector(search_space)})

    return best


if __name__ == '__main__':
    problem_size = 2
    search_space = [[-5, 5] for _ in range(problem_size)]
    max_gens = 150
    initial_population_size = 20
    number_of_clones = 10
    beta = 100
    number_of_random_cells_to_create = 2
    affinity_threashold = (search_space[0][1]-search_space[0][0])*0.05
    best = search(search_space, max_gens, initial_population_size,
                  number_of_clones, beta, number_of_random_cells_to_create, affinity_threashold)
    print(f"done! Solution: f={best['cost']}, s={best['vector']}")
