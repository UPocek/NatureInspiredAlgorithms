import math
import random


def objective_function(vector):
    return sum([x**2 for x in vector])


def random_vector(search_space):
    return [lower_bound + (upper_bound - lower_bound) * random.random() for lower_bound, upper_bound in search_space]


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


def mutate_vector(vector, stdevs, search_space):
    new_vector = [0] * len(vector)

    for i, x in enumerate(vector):
        new_vector[i] = x + stdevs[i] * random_gaussian()
        new_vector[i] = max(search_space[i][0], new_vector[i])
        new_vector[i] = min(search_space[i][1], new_vector[i])

    return new_vector


def mutate_strategy(stdevs):
    tau = math.sqrt(2.0 * len(stdevs))**-1.0
    tau_p = math.sqrt(2.0 * math.sqrt(len(stdevs)))**-1.0
    new_strategy = []
    for i in range(len(stdevs)):
        new_strategy.append(stdevs[i] * math.exp(tau_p * random_gaussian() +
                                                 tau * random_gaussian()))
    return new_strategy


def mutate(parent, search_space):
    new_chiild = {}
    new_chiild['vector'] = mutate_vector(
        parent['vector'], parent['strategy'], search_space)
    new_chiild['strategy'] = mutate_strategy(parent['strategy'])
    return new_chiild


def initialize_population(search_space, population_size):
    bounds = [(0, (search_space[i][1] - search_space[i][0]) * 0.05)
              for i in range(len(search_space))]

    population = [{}] * population_size

    for i in range(population_size):
        population[i]['vector'] = random_vector(search_space)
        population[i]['strategy'] = random_vector(bounds)
        population[i]['fitness'] = objective_function(population[i]['vector'])

    return population


def search(max_gens, search_space, population_size, number_of_children):
    population = initialize_population(search_space, population_size)
    population = sorted(population, key=lambda x: x['fitness'])
    best = population[0]

    for _ in range(max_gens):
        childern = [mutate(population[i], search_space)
                    for i in range(number_of_children)]

        for i, child in enumerate(childern):
            childern[i]['fitness'] = objective_function(child['vector'])

        union = childern + population
        union = sorted(union, key=lambda x: x['fitness'])

        if union[0]['fitness'] < best['fitness']:
            best = union[0]

        population = union[:population_size]

    return best


if __name__ == '__main__':
    problem_size = 2
    search_space = [[-5, 5] for _ in range(problem_size)]
    max_gens = 100
    population_size = 30
    number_of_childern = 20

    best = search(max_gens, search_space, population_size, number_of_childern)
    print(f"done! Solution: f={best['fitness']}, s={best['vector']}")
