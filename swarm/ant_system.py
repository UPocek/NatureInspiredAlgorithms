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


def initialize_pheromone_matrix(number_of_cities, naive_score):
    v = number_of_cities / naive_score
    return [[v for _ in range(number_of_cities)] for _ in range(number_of_cities)]


def calculate_choices(cities, city_from_index, visited, pheromone, c_heuristic, c_history):
    choices = []
    for city_to_index, coord in enumerate(cities):
        if city_to_index in visited:
            continue
        choice = {'city': city_to_index}
        choice['history'] = pheromone[city_from_index][city_to_index] ** c_history
        choice['distance'] = get_euclidean_distance(
            cities[city_from_index], coord)
        choice['heuristic'] = (1/choice['distance']) ** c_heuristic
        choice['probability_to_be_selected'] = choice['history'] * \
            choice['heuristic']
        choices.append(choice)
    return choices


def select_next_city(choices):
    sum = 0
    for choice in choices:
        sum += choice['probability_to_be_selected']
    if sum == 0:
        return choices[random.randint(0, len(choices)-1)]['city']
    v = random.random()

    for choice in choices:
        v -= choice['probability_to_be_selected'] / sum
        if v <= 0:
            return choice['city']

    return choices[-1]['city']


def stepwise_const(cities, pheromone, c_heuristic, c_history):
    new_path = []
    new_path.append(random.randint(0, len(cities)-1))

    while True:
        choices = calculate_choices(
            cities, new_path[-1], new_path, pheromone, c_heuristic, c_history)
        choices = sorted(
            choices, key=lambda x: x['probability_to_be_selected'], reverse=True)
        next_city = select_next_city(choices)
        new_path.append(next_city)
        if len(new_path) == len(cities):
            break
    return new_path


def decay_pheromone(pheromones, decay_factor):
    for pair in pheromones:
        for i, pheromone_strength in enumerate(pair):
            pair[i] = (1-decay_factor) * pheromone_strength


def update_pheromone(pheromone, solutions):
    for solution in solutions:
        for i, city_from_index in enumerate(solution['vector']):
            city_to_index = solution['vector'][0] if i == len(
                solution['vector'])-1 else solution['vector'][i+1]
            pheromone[city_from_index][city_to_index] += 1 / solution['cost']
            pheromone[city_to_index][city_from_index] += 1 / solution['cost']


def search(cities, max_iter, number_of_ants, decay_factor, c_heuristic, c_history):
    best = {'vector': generate_random_permutation(cities)}
    best['cost'] = get_cost(best['vector'], cities)
    pheromone = initialize_pheromone_matrix(len(cities), best['cost'])
    for _ in range(max_iter):
        solutions = []
        for _ in range(number_of_ants):
            candidate = {}
            candidate['vector'] = stepwise_const(
                cities, pheromone, c_heuristic, c_history)
            candidate['cost'] = get_cost(candidate['vector'], cities)
            solutions.append(candidate)
            if candidate['cost'] < best['cost']:
                best = candidate
        decay_pheromone(pheromone, decay_factor)
        update_pheromone(pheromone, solutions)
    return best


if __name__ == '__main__':
    berlin52 = [[565, 575], [25, 185], [345, 750], [945, 685], [845, 655], [880, 660], [25, 230], [525, 1000], [580, 1175], [650, 1130], [1605, 620], [1220, 580], [1465, 200], [1530, 5], [845, 680], [725, 370], [145, 665], [415, 635], [510, 875], [560, 365], [300, 465], [520, 585], [480, 415], [835, 625], [975, 580], [1215, 245], [
        1320, 315], [1250, 400], [660, 180], [410, 250], [420, 555], [575, 665], [1150, 1160], [700, 580], [685, 595], [685, 610], [770, 610], [795, 645], [720, 635], [760, 650], [475, 960], [95, 260], [875, 920], [700, 500], [555, 815], [830, 485], [1170, 65], [830, 610], [605, 625], [595, 360], [1340, 725], [1740, 245]]
    max_iter = 50
    number_of_ants = len(berlin52)
    decay_factor = 0.8
    c_heuristic = 2.5
    c_history = 1.0

    best = search(berlin52, max_iter, number_of_ants,
                  decay_factor, c_heuristic, c_history)
    print(f"Done. Best Solution: c={best['cost']}, v={best['vector']}")
