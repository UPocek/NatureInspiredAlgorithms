import random


def objective_function(vector):
    return sum([x**2 for x in vector])


def random_within_search_space(lower_bound, upper_bound):
    return lower_bound + (upper_bound-lower_bound) * random.random()


def generate_random_vector(search_space):
    return [random_within_search_space(lower_bound, upper_bound) for lower_bound, upper_bound in search_space]


def mutate_with_information(candidate, beliefs, search_space):
    new_vector = [0] * len(candidate['vector'])
    for i in range(len(candidate['vector'])):
        new_vector[i] = random_within_search_space(
            beliefs['normative'][i][0], beliefs['normative'][i][1])
        new_vector[i] = max(new_vector[i], search_space[i][0])
        new_vector[i] = min(new_vector[i], search_space[i][1])

    return {'vector': new_vector}


def binary_tournament(population):
    i, j = random.randint(0, len(population) -
                          1), random.randint(0, len(population)-1)
    while j == i:
        j = random.randint(0, len(population)-1)
    return population[i] if population[i]['fitness'] < population[j]['fitness'] else population[j]


def initialize_beliefspace(search_space):
    beliefspace = {}
    beliefspace['situational'] = None
    beliefspace['normative'] = [search_space[i]
                                for i in range(len(search_space))]

    return beliefspace


def update_beliefspace_situational(beliefspace, best_individual):
    current_leader = beliefspace['situational']
    if current_leader == None or best_individual['fitness'] < current_leader['fitness']:
        beliefspace['situational'] = best_individual


def update_beliefspace_normative(beliefspace, newly_accepted_beliefs):
    for i, normative_beliefspace_bounds in enumerate(beliefspace['normative']):
        normative_beliefspace_bounds[0] = min(
            newly_accepted_beliefs, key=lambda x: x['vector'][i])['vector'][i]
        normative_beliefspace_bounds[1] = max(
            newly_accepted_beliefs, key=lambda x: x['vector'][i])['vector'][i]


def search(max_gens, search_space, population_size, number_of_accepted_beliefs):
    population = [{'vector': generate_random_vector(
        search_space)} for _ in range(population_size)]

    beliefspace = initialize_beliefspace(search_space)

    for individual in population:
        individual['fitness'] = objective_function(individual['vector'])

    population = sorted(population, key=lambda x: x['fitness'])
    best = population[0]

    update_beliefspace_situational(beliefspace, best)

    for _ in range(max_gens):
        children = [mutate_with_information(
            individual, beliefspace, search_space) for individual in population]
        for child in children:
            child['fitness'] = objective_function(child['vector'])

        children = sorted(children, key=lambda x: x['fitness'])
        best = children[0]

        update_beliefspace_situational(beliefspace, best)
        population = [binary_tournament(
            population + children) for _ in range(population_size)]

        population = sorted(population, key=lambda x: x['fitness'])
        accepted = population[:number_of_accepted_beliefs]

        update_beliefspace_normative(beliefspace, accepted)

    return beliefspace['situational']


if __name__ == '__main__':
    problem_size = 2
    search_space = [[-5, 5] for _ in range(problem_size)]
    max_gens = 200
    population_size = 100
    number_of_accepted_beliefs = round(population_size * 0.2)

    best = search(max_gens, search_space, population_size,
                  number_of_accepted_beliefs)

    print(f"done! Solution: f={best['fitness']}, s={best['vector']}")
