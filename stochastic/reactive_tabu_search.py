from math import sqrt
import random


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


def is_tabu(edge, tabu_list, iter, prohib_period):
    for entry in tabu_list:
        if entry['edge'] == edge:
            if iter - entry['iter'] <= prohib_period:
                return True
            else:
                return False
    return False


def make_tabu(tabu_list, edge, iter):
    for entry in tabu_list:
        if entry['edge'] == edge:
            entry['iter'] = iter
            return
    new_entry = {}
    new_entry['edge'] = edge
    new_entry['iter'] = iter


def to_edge_list(permutation):
    edge_list = []
    for i, city_from_index in enumerate(permutation):
        city_to_index = permutation[i +
                                    1] if i != len(permutation) - 1 else permutation[0]
        if city_to_index < city_from_index:
            city_to_index, city_from_index = city_from_index, city_to_index
        edge_list.append([city_from_index, city_to_index])
    return edge_list


def are_equivalent(permutation1, permutation2):
    for index1, index2 in zip(permutation1, permutation2):
        if index1 != index2:
            return False
    return True


def generate_candidate(best, cities):
    candidate = {}
    candidate['vector'], edges = stochastic_two_opt_with_tabu(best['vector'])
    candidate['cost'] = get_cost(candidate['vector'], cities)
    return candidate, edges


def get_candidate_entry(visited_list, permutation):
    edge_list = to_edge_list(permutation)
    for el in visited_list:
        if are_equivalent(edge_list, el['edge_list']):
            return el
    return None


def store_permutation(visited_list, permutation, iteration):
    entry = {}
    entry['edge_list'] = to_edge_list(permutation)
    entry['iter'] = iteration
    entry['visits'] = 1
    visited_list.append(entry)


def sort_neighborhood(candidates, tabu_list, prohib_period, iteration):
    tabu, admissable = [], []

    for candidate in candidates:
        if is_tabu(candidate[1][0], tabu_list, iteration, prohib_period) or is_tabu(candidate[1][1], tabu_list, iteration, prohib_period):
            tabu.append(candidate)
        else:
            admissable.append(candidate)
    return tabu, admissable


def reactive_tabu_search(cities, max_cand, max_iter, increase, decrease):
    best = {}
    best['vector'] = generate_random_permutation(cities)
    best['cost'] = get_cost(best['vector'], cities)
    tabu_list, prohib_period = [], 1
    visited_list, avg_size, iter_of_last_change_of_prohib_period = [], 1, 0

    for iter in range(max_iter):
        candidate_entry = get_candidate_entry(visited_list, best['vector'])
        if candidate_entry is not None:
            repetation_interval = iter - candidate_entry['iter']
            if repetation_interval < 2 * (len(cities)):
                avg_size = 0.1 * \
                    (iter - candidate_entry['iter']) + 0.9 * avg_size
                prohib_period *= increase
                iter_of_last_change_of_prohib_period = iter
            candidate_entry['iter'] = iter
            candidate_entry['visits'] += 1
        else:
            store_permutation(visited_list, best['vector'], iter)

        if iter - iter_of_last_change_of_prohib_period > avg_size:
            prohib_period = max(prohib_period * decrease, 1)
            iter_of_last_change_of_prohib_period = iter

        candidates = []
        for _ in range(max_cand):
            candidates.append(generate_candidate(best, cities))

        candidates = sorted(candidates, key=lambda x: x[0]['cost'])

        tabu, admissable = sort_neighborhood(
            candidates, tabu_list, prohib_period, iter)

        best, best_move_edges = tabu[0] if len(
            admissable) == 0 else admissable[0]

        if admissable:
            if admissable[0][0]['cost'] < best['cost']:
                best, best_move_edges = admissable[0]
        elif tabu:
            if tabu[0][0]['cost'] < best['cost']:
                best, best_move_edges = tabu[0]
        else:
            if candidates[0][0]['cost'] < best['cost']:
                best = candidates[0][0]

        for edge in best_move_edges:
            make_tabu(tabu_list, edge, iter)

    return best


if __name__ == '__main__':
    berlin52 = [[565, 575], [25, 185], [345, 750], [945, 685], [845, 655], [880, 660], [25, 230], [525, 1000], [580, 1175], [650, 1130], [1605, 620], [1220, 580], [1465, 200], [1530, 5], [845, 680], [725, 370], [145, 665], [415, 635], [510, 875], [560, 365], [300, 465], [520, 585], [480, 415], [835, 625], [975, 580], [1215, 245], [
        1320, 315], [1250, 400], [660, 180], [410, 250], [420, 555], [575, 665], [1150, 1160], [700, 580], [685, 595], [685, 610], [770, 610], [795, 645], [720, 635], [760, 650], [475, 960], [95, 260], [875, 920], [700, 500], [555, 815], [830, 485], [1170, 65], [830, 610], [605, 625], [595, 360], [1340, 725], [1740, 245]]
    max_iter = 10000
    max_candidates = 75
    increase = 1.3
    decrease = 0.9

    best = reactive_tabu_search(
        berlin52, max_candidates, max_iter, increase, decrease)

    print(f"Done. Best Solution: c={best['cost']}, v={best['vector']}")
