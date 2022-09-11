import math
import random


def get_euclidean_distance(city_from, city_to):
    return round(math.sqrt((city_from[0] - city_to[0])**2 + (city_from[1] - city_to[1])**2))


def cost(permutation, cities):
    distance = 0
    for i, city_from_index in enumerate(permutation):
        city_to_index = permutation[i +
                                    1] if i != len(permutation) - 1 else permutation[0]
        distance += get_euclidean_distance(
            cities[city_from_index], cities[city_to_index])

    return distance


def generate_random_permutation(cities):
    indices = list(range(len(cities)))
    random.shuffle(indices)
    return indices


def calculate_neighbor_rank(city_number, cities, ignore=[]):
    neighbors = []
    for i, city in enumerate(cities):
        if i == city_number or city in ignore:
            continue
        neighbor = {'number': i}
        neighbor['distance'] = get_euclidean_distance(
            cities[city_number], city)
        neighbors.append(neighbor)
    return sorted(neighbors, key=lambda x: x['distance'])


def get_edges_for_city(city_number, permutation):
    city_before_number, city_after_number = None, None
    for i, city_index in enumerate(permutation):
        if city_index == city_number:
            city_before_number = permutation[i -
                                             1] if i != 0 else permutation[-1]
            city_after_number = permutation[i +
                                            1] if i != len(permutation)-1 else permutation[0]
            break
    return city_before_number, city_after_number


def calculate_city_fitness(permutation, city_number, cities):
    city_before_number, city_after_number = get_edges_for_city(
        city_number, permutation)
    neighbors = calculate_neighbor_rank(city_number, cities)
    neighbor_before, neighbor_after = -1, -1
    for i, neighbor in enumerate(neighbors):
        if neighbor['number'] == city_before_number:
            neighbor_before = i + 1
        if neighbor['number'] == city_after_number:
            neighbor_after = i + 1
        if neighbor_before != -1 and neighbor_after != -1:
            break
    return 3 / (neighbor_before + neighbor_after)


def calculate_city_fitnesses(cities, permutation):
    city_fitnesses = []
    for i in range(len(cities)):
        city_fitness = {'number': i}
        city_fitness['fitness'] = calculate_city_fitness(
            permutation, city_fitness['number'], cities)
        city_fitnesses.append(city_fitness)

    return sorted(city_fitnesses, key=lambda x: x['fitness'])


def calculate_component_probabilities(ordered_components, tau):
    sum = 0
    for i, component in enumerate(ordered_components):
        component['probability'] = (i+1)**(-tau)
        sum += component['probability']
    return sum


def make_selection(components, sum_probability):
    selection = random.random()
    for component in components:
        selection -= (component['probability'] / sum_probability)
        if selection <= 0:
            return component['number']
    return components[-1]['number']


def probabilistic_selection(ordered_components, tau, exclude=[]):
    sum = calculate_component_probabilities(ordered_components, tau)
    selected_city_number = None
    while True:
        selected_city_number = make_selection(ordered_components, sum)
        if not selected_city_number in exclude:
            break
    return selected_city_number


def vary_permutation(permutation, selected_city_number, new_neighbor, further_edge):
    perm = [el for el in permutation]
    c1, c2 = perm.index(selected_city_number), perm.index(new_neighbor)

    if c1 == len(perm)-1:
        right_city = 0
    else:
        right_city = c1 + 1

    if c1 > c2:
        c1, c2 = c2, c1

    if perm[right_city] == further_edge:
        perm[c1+1:c2+1] = reversed(perm[c1+1:c2+1])
    else:
        perm[c1:c2] = reversed(perm[c1:c2])

    return perm


def get_further_edge(edges, neighbors):
    n1 = [x for x in neighbors if x['number'] == edges[0]]
    n2 = [x for x in neighbors if x['number'] == edges[1]]
    return n1[0]['number'] if n1[0]['distance'] > n2[0]['distance'] else n2[0]['distance']


def generate_new_permutation(cities, tau, permutation):
    city_fitnesses = calculate_city_fitnesses(cities, permutation)
    selected_city_number = probabilistic_selection(
        list(reversed(city_fitnesses)), tau)
    neighbors = calculate_neighbor_rank(selected_city_number, cities)
    edges = get_edges_for_city(selected_city_number, permutation)
    new_neighbor = probabilistic_selection(neighbors, tau, edges)
    further_edge = get_further_edge(edges, neighbors)
    return vary_permutation(permutation, selected_city_number, new_neighbor, further_edge)


def search(cities, max_iter, tau):
    current = {'vector': generate_random_permutation(cities)}
    current['cost'] = cost(current['vector'], cities)
    best = current
    for _ in range(max_iter):
        candidate = {}
        candidate['vector'] = generate_new_permutation(
            cities, tau, current['vector'])
        candidate['cost'] = cost(candidate['vector'], cities)
        current = candidate
        if current['cost'] < best['cost']:
            best = current

    return best


if __name__ == '__main__':
    berlin52 = [[565, 575], [25, 185], [345, 750], [945, 685], [845, 655], [880, 660], [25, 230], [525, 1000], [580, 1175], [650, 1130], [1605, 620], [1220, 580], [1465, 200], [1530, 5], [845, 680], [725, 370], [145, 665], [415, 635], [510, 875], [560, 365], [300, 465], [520, 585], [480, 415], [835, 625], [975, 580], [1215, 245], [
        1320, 315], [1250, 400], [660, 180], [410, 250], [420, 555], [575, 665], [1150, 1160], [700, 580], [685, 595], [685, 610], [770, 610], [795, 645], [720, 635], [760, 650], [475, 960], [95, 260], [875, 920], [700, 500], [555, 815], [830, 485], [1170, 65], [830, 610], [605, 625], [595, 360], [1340, 725], [1740, 245]]
    max_iter = 250
    tau = 1.6
    best = search(berlin52, max_iter, tau)
    print(f"Done. Best Solution: c={best['cost']}, v={best['vector']}")
