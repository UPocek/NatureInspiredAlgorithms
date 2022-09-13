import random


def objective_function(vector):
    return sum([x**2 for x in vector])


def random_vector(search_space):
    return [lower_bound + (upper_bound - lower_bound) * random.random() for lower_bound, upper_bound in search_space]


def create_random_bee(search_space):
    return {'vector': random_vector(search_space)}


def local_search_neighborhood(site, path_size, search_space):
    vector = []
    for i, x in enumerate(site):
        x = x + random.random() * path_size if random.random() < 0.5 else x - \
            random.random() * path_size
        x = max(x, search_space[i][0])
        x = min(x, search_space[i][1])
        vector.append(x)
    return {'vector': vector}


def search_neighborhood(parent, neighborhood_size, patch_size, search_space):
    neighborhood = []
    for _ in range(neighborhood_size):
        neighborhood.append(local_search_neighborhood(
            parent['vector'], patch_size, search_space))
    for point in neighborhood:
        point['fitness'] = objective_function(point['vector'])

    return sorted(neighborhood, key=lambda x: x['fitness'])[0]


def create_scout_bees(search_space, num_scouts):
    return [create_random_bee(search_space)for _ in range(num_scouts)]


def search(max_gens, search_space, num_bees, num_sites, elite_sites, patch_size, elite_bees, ordinary_bees):
    best = None
    population = [create_random_bee(search_space) for _ in range(num_bees)]
    for _ in range(max_gens):
        for bee in population:
            bee['fitness'] = objective_function(bee['vector'])

        population = sorted(population, key=lambda x: x['fitness'])
        if best is None or population[0]['fitness'] < best['fitness']:
            best = population[0]

        searched_patches = []
        for i, top_bee in enumerate(population[:num_sites]):
            neighborhood_size = elite_bees if i < elite_sites else ordinary_bees
            searched_patches.append(search_neighborhood(
                top_bee, neighborhood_size, patch_size, search_space))
        new_patches = create_scout_bees(search_space, (num_bees-num_sites))
        population = searched_patches + new_patches
        patch_size = patch_size * 0.95
    return best


if __name__ == '__main__':
    problem_size = 3
    search_space = [[-5, 5] for _ in range(problem_size)]
    max_gens = 500
    num_bees = 45
    num_sites = 3
    elite_sites = 1
    patch_size = 3
    elite_bees = 7
    ordinary_bees = 2

    best = search(max_gens, search_space, num_bees, num_sites, elite_sites,
                  patch_size, elite_bees, ordinary_bees)
    print(f"done! Solution: f={best['fitness']}, s={best['vector']}")
