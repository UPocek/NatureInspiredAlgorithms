import random


def objective_function(vector):
    return sum([x**2 for x in vector])


def random_vector(search_space):
    return [lower_bound + (upper_bound - lower_bound) * random.random() for lower_bound, upper_bound in search_space]


def de_rand_1_bin(current, parent1, parent2, parent_to_be_changed, weight, crossover_rate, search_space):
    sample = {'vector': [0] * len(current)}

    cut = random.randint(0, len(sample['vector']) - 2) + 1

    for i in range(len(sample['vector'])):
        sample['vector'][i] = current['vector'][i]

        if i == cut or random.random() < crossover_rate:
            v = parent_to_be_changed['vector'][i] + weight * \
                (parent1['vector'][i] - parent2['vector'][i])
            v = max(search_space[i][0], v)
            v = min(search_space[i][1], v)
            sample['vector'][i] = v

    return sample


def select_parents(population, current):
    p1, p2, p3 = random.randint(0, len(population) - 1), random.randint(
        0, len(population) - 1), random.randint(0, len(population) - 1)

    while p1 == current:
        p1 = random.randint(0, len(population) - 1)

    while p2 != current and p2 != p1:
        p2 = random.randint(0, len(population) - 1)

    while p3 != current and p3 != p2 and p3 != p1:
        p3 = random.randint(0, len(population) - 1)

    return p1, p2, p3


def create_children(population, search_space, weight, crossover_rate):
    children = []
    for i, current in enumerate(population):
        p1, p2, p3 = select_parents(population, i)
        children.append(de_rand_1_bin(
            current, population[p1], population[p2], population[p3], weight, crossover_rate, search_space))

    return children


def select_population(parents, children):
    new_population = []
    for i in range(len(parents)):
        new_population.append(
            children[i] if children[i]['fitness'] <= parents[i]['fitness'] else parents[i])

    return new_population


def search(max_gens, search_space, population_size, weight, crossover_rate):
    population = [{'vector': random_vector(
        search_space)} for _ in range(population_size)]

    for i, individual in enumerate(population):
        population[i]['fitness'] = objective_function(individual['vector'])

    population = sorted(population, key=lambda x: x['fitness'])
    best = population[0]

    for _ in range(max_gens):
        children = create_children(
            population, search_space, weight, crossover_rate)
        for i, child in enumerate(children):
            children[i]['fitness'] = objective_function(child['vector'])
        population = select_population(population, children)
        population = sorted(population, key=lambda x: x['fitness'])

        if population[0]['fitness'] <= best['fitness']:
            best = population[0]

    return best


if __name__ == '__main__':

    # f = sum(xi**2), i = {1,2...n}, -5 <= xi <= 5

    problem_size = 3
    search_space = [[-5, 5] for _ in range(problem_size)]

    max_gens = 200
    population_size = 10*problem_size
    weightf = 0.8
    crossf = 0.9

    best = search(max_gens, search_space, population_size, weightf, crossf)
    print(f"done! Solution: f={best['fitness']}, s=#{best['vector']}")
