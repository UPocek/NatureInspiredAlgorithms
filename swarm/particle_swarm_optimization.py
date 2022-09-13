import random


def objective_function(vector):
    return sum([x**2 for x in vector])


def random_vector(search_space):
    return [lower_bound + (upper_bound - lower_bound) * random.random() for lower_bound, upper_bound in search_space]


def create_particle(search_space, velocity_space):
    particle = {}
    particle['position'] = random_vector(search_space)
    particle['cost'] = objective_function(particle['position'])
    particle['personal_best_position'] = [x for x in particle['position']]
    particle['personal_best_cost'] = particle['cost']
    particle['velocity'] = random_vector(velocity_space)
    return particle


def get_global_best(population, current_global_best=None):
    population = sorted(population, key=lambda x: x['cost'])
    best = population[0]

    if current_global_best is None or best['cost'] <= current_global_best['cost']:
        current_global_best = {}
        current_global_best['position'] = [x for x in best['position']]
        current_global_best['cost'] = best['cost']
    return current_global_best


def update_velocity(particle, global_best, max_velocity, c1, c2):
    for i, v in enumerate(particle['velocity']):
        v1 = c1 * random.random() * \
            (particle['personal_best_position'][i] - particle['position'][i])
        v2 = c2 * random.random() * \
            (global_best['position'][i] - particle['position'][i])
        particle['velocity'][i] = v + v1 + v2
        particle['velocity'][i] = max(particle['velocity'][i], -max_velocity)
        particle['velocity'][i] = min(particle['velocity'][i], max_velocity)


def update_position(part, search_space):
    for i, x in enumerate(part['position']):
        part['position'][i] = x + part['velocity'][i]
        if part['position'][i] > search_space[i][1]:
            part['position'][i] = search_space[i][1] - \
                abs(part['position'][i] - search_space[i][1])
            part['velocity'][i] *= -1
        elif part['position'][i] < search_space[i][0]:
            part['position'][i] = search_space[i][0] + \
                abs(part['position'][i] - search_space[i][0])
            part['velocity'][i] *= -1


def update_personal_best_position(particle):
    if particle['cost'] > particle['personal_best_cost']:
        return
    particle['personal_best_cost'] = particle['cost']
    particle['personal_best_position'] = [x for x in particle['position']]


def search(max_gens, search_space, velocity_space, population_size, max_velocity, c1, c2):
    population = [create_particle(search_space, velocity_space)
                  for _ in range(population_size)]
    global_best = get_global_best(population)

    for _ in range(max_gens):
        for particle in population:
            update_velocity(particle, global_best, max_velocity, c1, c2)
            update_position(particle, search_space)
            particle['cost'] = objective_function(particle['position'])
            update_personal_best_position(particle)
        global_best = get_global_best(population, global_best)

    return global_best


if __name__ == '__main__':
    problem_size = 2
    search_space = [[-5, 5] for _ in range(problem_size)]
    velocity_space = [[-1, 1] for _ in range(problem_size)]
    max_gens = 100
    population_size = 50
    max_velocity = 100
    c1, c2 = 2, 2

    best = search(max_gens, search_space, velocity_space,
                  population_size, max_velocity, c1, c2)
    print(f"done! Solution: f={best['cost']}, s={best['position']}")
