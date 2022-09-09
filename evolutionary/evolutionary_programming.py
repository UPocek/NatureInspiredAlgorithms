import random
import math


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


def mutate(candidate, search_space):
    child = {'vector': [], 'strategy': []}

    for i, x_old in enumerate(candidate['vector']):
        s_old = candidate['strategy'][i]
        x = x_old + s_old * random_gaussian()
        x = max(search_space[i][0], x)
        x = min(search_space[i][1], x)
        child['vector'].append(x)
        child['strategy'].append(s_old + random_gaussian() * abs(s_old)**0.5)

    return child


def initialize_population(search_space, population_size):
    bounds = [(0, (search_space[i][1] - search_space[i][0]) * 0.05)
              for i in range(len(search_space))]

    population = [{}] * population_size

    for i in range(population_size):
        population[i]['vector'] = random_vector(search_space)
        population[i]['strategy'] = random_vector(bounds)
        population[i]['fitness'] = objective_function(population[i]['vector'])

    return population


def tournament(candidate, population, number_of_individuals_to_compete):
    candidate['wins'] = 0
    for _ in range(number_of_individuals_to_compete):
        other = population[random.randint(0, len(population) - 1)]
        if candidate['fitness'] < other['fitness']:
            candidate['wins'] += 1


def search(max_gens, search_space, population_size, bout_size):
    population = initialize_population(search_space, population_size)
    population = sorted(population, key=lambda x: x['fitness'])
    best = population[0]

    for _ in range(max_gens):
        children = [mutate(candidate, search_space)
                    for candidate in population]
        for i, child in enumerate(children):
            children[i]['fitness'] = objective_function(child['vector'])
        children = sorted(children, key=lambda x: x['fitness'])

        if children[0]['fitness'] < best['fitness']:
            best = children[0]

        union = children+population
        for individual in union:
            tournament(individual, population, bout_size)

        union = sorted(union, key=lambda x: x['wins'])

        population = union[:population_size]

    return best


if __name__ == '__main__':

    # f = sum(xi**2), i = {1,2...n}, -5 <= xi <= 5

    problem_size = 2
    search_space = [[-5, 5] for _ in range(problem_size)]

    max_gens = 200
    population_size = 100
    bout_size = 5

    best = search(max_gens, search_space, population_size, bout_size)

    print(f"done! Solution: f={best['fitness']}, s={best['vector']}")
