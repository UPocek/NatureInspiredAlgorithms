import random
from math import sqrt


def get_euclidean_distance(city_from, city_to):
    return round(sqrt((city_from[0] - city_to[0])**2 + (city_from[1] - city_to[1])**2))


def get_cost(permutation, cities):
    distance = 0

    for i, city_from_index in enumerate(permutation):
        city_to_index = permutation[i +
                                    1] if i != len(permutation) - 1 else permutation[0]
        distance += get_euclidean_distance(
            cities[city_from_index], cities[city_to_index])

    return distance


def generate_random_permutation(cities):
    indices = list(range(0, len(cities)))
    random.shuffle(indices)
    return indices


def stochastic_two_opt_with_tabu(permutation):
    perm = [el for el in permutation]

    city_from_index, city_to_index = random.randint(
        0, len(perm) - 1), random.randint(0, len(perm) - 1)

    exclude = [city_from_index]
    if city_from_index == 0:
        exclude.append(len(perm) - 1)
    else:
        exclude.append(city_from_index - 1)
    if city_from_index == len(perm) - 1:
        exclude.append(0)
    else:
        exclude.append(city_from_index + 1)

    while city_to_index in exclude:
        city_to_index = random.randint(0, len(perm) - 1)

    if city_to_index < city_from_index:
        city_to_index, city_from_index = city_from_index, city_to_index

    reverse_slice = [el for el in perm[city_from_index:city_to_index]]
    reverse_slice.reverse()

    perm[city_from_index:city_to_index] = reverse_slice

    return perm, [[permutation[city_from_index-1], permutation[city_from_index]], [permutation[city_to_index-1], permutation[city_to_index]]]


def is_tabu(permutation, tabu_list):
    for i, city_from_index in enumerate(permutation):
        city_to_index = permutation[i +
                                    1] if i != len(permutation) - 1 else permutation[0]
        for forbidden_edge in tabu_list:
            if forbidden_edge == [city_from_index, city_to_index]:
                return True
    return False


def generate_candidate(best, tabu_list, cities):
    perm, edges = None, None
    while perm == None or is_tabu(perm, tabu_list):
        perm, edges = stochastic_two_opt_with_tabu(best['vector'])

    candidate = {}
    candidate['vector'] = perm
    candidate['cost'] = get_cost(candidate['vector'], cities)
    return candidate, edges


def tabu_search(cities, tabu_list_size, candidate_list_size, max_iter):
    best = {}
    best['vector'] = generate_random_permutation(cities)
    best['cost'] = get_cost(best['vector'], cities)
    tabu_queue = [[0, 0]] * tabu_list_size

    for _ in range(max_iter):
        candidates = []
        for _ in range(candidate_list_size):
            candidates.append(generate_candidate(best, tabu_queue, cities))
        candidates = sorted(candidates, key=lambda x: x[0]['cost'])
        best_candidate = candidates[0][0]
        best_candidate_edges = candidates[0][1]
        if best_candidate['cost'] < best['cost']:
            best = best_candidate
            for edge in best_candidate_edges:
                tabu_queue.pop(0)
                tabu_queue.append(edge)

    return best


if __name__ == '__main__':
    berlin52 = [[565, 575], [25, 185], [345, 750], [945, 685], [845, 655], [880, 660], [25, 230], [525, 1000], [580, 1175], [650, 1130], [1605, 620], [1220, 580], [1465, 200], [1530, 5], [845, 680], [725, 370], [145, 665], [415, 635], [510, 875], [560, 365], [300, 465], [520, 585], [480, 415], [835, 625], [975, 580], [1215, 245], [
        1320, 315], [1250, 400], [660, 180], [410, 250], [420, 555], [575, 665], [1150, 1160], [700, 580], [685, 595], [685, 610], [770, 610], [795, 645], [720, 635], [760, 650], [475, 960], [95, 260], [875, 920], [700, 500], [555, 815], [830, 485], [1170, 65], [830, 610], [605, 625], [595, 360], [1340, 725], [1740, 245]]
    max_iter = 1000
    tabu_list_size = 15
    candidate_list_size = 75

    best = tabu_search(berlin52, tabu_list_size, candidate_list_size, max_iter)
    print(f"Done. Best Solution: c={best['cost']}, v={best['vector']}")
