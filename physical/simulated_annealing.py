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


def stochastic_two_opt(permutation):
    city_from_index, city_to_index = random.randint(
        0, len(permutation)-1), random.randint(0, len(permutation)-1)
    exclude = [city_from_index]
    if city_from_index == 0:
        exclude.append(len(permutation)-1)
    else:
        exclude.append(city_from_index-1)
    if city_from_index == len(permutation)-1:
        exclude.append(0)
    else:
        exclude.append(city_from_index+1)
    while city_to_index == city_from_index:
        city_to_index = random.randint(0, len(permutation)-1)

    if city_to_index < city_from_index:
        city_from_index, city_to_index = city_to_index, city_from_index

    permutation[city_from_index:city_to_index] = reversed(
        permutation[city_from_index:city_to_index])


def create_neighbor(current, cities):
    candidate = {}
    candidate['vector'] = [el for el in current['vector']]
    stochastic_two_opt(candidate['vector'])
    candidate['cost'] = cost(candidate['vector'], cities)
    return candidate


def should_accept(new_candidate, current_candidate, temperature):
    if new_candidate['cost'] <= current_candidate['cost']:
        return True
    return math.exp((current_candidate['cost'] - new_candidate['cost']) / temperature) > random.random()


def search(cities, max_iter, max_temperature, temperature_change):
    current = {'vector': generate_random_permutation(cities)}
    current['cost'] = cost(current['vector'], cities)
    temperature = max_temperature
    best = current

    for _ in range(max_iter):
        candidate = create_neighbor(current, cities)
        temperature = temperature * temperature_change
        if should_accept(candidate, current, temperature):
            current = candidate
            if candidate['cost'] < best['cost']:
                best = candidate

    return best


if __name__ == '__main__':
    berlin52 = [[565, 575], [25, 185], [345, 750], [945, 685], [845, 655], [880, 660], [25, 230], [525, 1000], [580, 1175], [650, 1130], [1605, 620], [1220, 580], [1465, 200], [1530, 5], [845, 680], [725, 370], [145, 665], [415, 635], [510, 875], [560, 365], [300, 465], [520, 585], [480, 415], [835, 625], [975, 580], [1215, 245], [
        1320, 315], [1250, 400], [660, 180], [410, 250], [420, 555], [575, 665], [1150, 1160], [700, 580], [685, 595], [685, 610], [770, 610], [795, 645], [720, 635], [760, 650], [475, 960], [95, 260], [875, 920], [700, 500], [555, 815], [830, 485], [1170, 65], [830, 610], [605, 625], [595, 360], [1340, 725], [1740, 245]]
    max_iter = 2000
    max_temperature = 100000
    temperature_change = 0.98

    best = search(berlin52, max_iter, max_temperature, temperature_change)
    print(f"Done. Best Solution: c={best['cost']}, v={best['vector']}")
