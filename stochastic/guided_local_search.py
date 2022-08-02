import random
from math import sqrt


def get_euclidean_distance(city_from, city_to):
    return round(sqrt((city_from[0] - city_to[0])**2 + (city_from[1] - city_to[1])**2))


def get_cost_and_augmentation(permutation, penalties, cities, lambda_factor):
    total_distance, augmented = 0, 0

    for i, city_from_index in enumerate(permutation):
        city_to_index = permutation[i +
                                    1] if i != len(permutation) - 1 else permutation[0]
        distance = get_euclidean_distance(
            cities[city_from_index], cities[city_to_index])
        total_distance += distance
        augmented += distance + lambda_factor * \
            penalties[city_from_index][city_to_index]

    return total_distance, augmented


def generate_random_permutation(cities):
    indices = list(range(0, len(cities)))
    random.shuffle(indices)
    return indices


def stochastic_two_opt(permutation):
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

    return perm


def local_search(current, cities, penalties, max_no_impr, lambda_factor):
    count = 0
    current['cost'], current['aug_cost'] = get_cost_and_augmentation(
        current['vector'], penalties, cities, lambda_factor)

    while count < max_no_impr:
        candidate = {}
        candidate['vector'] = stochastic_two_opt(current['vector'])
        candidate['cost'], candidate['aug_cost'] = get_cost_and_augmentation(
            candidate['vector'], penalties, cities, lambda_factor)
        if candidate['aug_cost'] < current['aug_cost']:
            current = candidate
            count = 0
        else:
            count += 1

    return current


def calculate_feature_utilities(penal, cities, permutation):
    utilities = [0] * len(permutation)

    for i, city_from_index in enumerate(permutation):
        city_to_index = permutation[i +
                                    1] if i != len(permutation) - 1 else permutation[0]
        utilities[i] += get_euclidean_distance(
            cities[city_from_index], cities[city_to_index]) / (1.0 + penal[city_from_index][city_to_index])
    return utilities


def get_new_penalties(penalties, permutation, utilities):
    max_util = max(utilities)

    for i, city_from_index in enumerate(permutation):
        city_to_index = permutation[i +
                                    1] if i != len(permutation) - 1 else permutation[0]
        if utilities[i] == max_util:
            penalties[city_from_index][city_to_index] += 1

    return penalties


def guided_local_search(max_iter, cities, max_no_impr, lambda_factor):
    current = {}
    current['vector'] = generate_random_permutation(cities)
    best = None
    penalties = [[0] * len(cities)] * len(cities)

    for _ in range(max_iter):
        current = local_search(current, cities, penalties,
                               max_no_impr, lambda_factor)
        utilities = calculate_feature_utilities(
            penalties, cities, current['vector'])
        penalties = get_new_penalties(penalties, current['vector'], utilities)

        if best is None or current['cost'] < best['cost']:
            best = current

    return best


if __name__ == '__main__':
    berlin52 = [[565, 575], [25, 185], [345, 750], [945, 685], [845, 655], [880, 660], [25, 230], [525, 1000], [580, 1175], [650, 1130], [1605, 620], [1220, 580], [1465, 200], [1530, 5], [845, 680], [725, 370], [145, 665], [415, 635], [510, 875], [560, 365], [300, 465], [520, 585], [480, 415], [835, 625], [975, 580], [1215, 245], [
        1320, 315], [1250, 400], [660, 180], [410, 250], [420, 555], [575, 665], [1150, 1160], [700, 580], [685, 595], [685, 610], [770, 610], [795, 645], [720, 635], [760, 650], [475, 960], [95, 260], [875, 920], [700, 500], [555, 815], [830, 485], [1170, 65], [830, 610], [605, 625], [595, 360], [1340, 725], [1740, 245]]
    max_iter = 1000
    max_no_impr = 30
    alpha = 0.3

    local_search_optima = sum([get_euclidean_distance(
        berlin52[i-1], berlin52[i]) for i in range(1, len(berlin52))])
    lambda_factor = alpha * (local_search_optima / len(berlin52))

    best = guided_local_search(max_iter, berlin52, max_no_impr, lambda_factor)
    print(f"Done. Best Solution: c={best['cost']}, v={best['vector']}")
