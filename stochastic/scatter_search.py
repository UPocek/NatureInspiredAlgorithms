from math import sqrt
import random


def objective_function(vector):
    return sum([x**2 for x in vector])


def random_within_bounds(lower_bound, upper_bound):
    return lower_bound + (upper_bound-lower_bound) * random.random()


def generate_random_vector(search_space):
    return [random_within_bounds(lower_bound, upper_bound) for lower_bound, upper_bound in search_space]


def take_step(search_space, current_position, step_size):
    finish_position = [0] * len(current_position)

    for i in range(len(finish_position)):
        position_min = max(search_space[i][0], current_position[i] - step_size)
        position_max = min(search_space[i][1], current_position[i] + step_size)
        finish_position[i] = position_min + \
            (position_max - position_min) * random.random()

    return finish_position


def local_search(best, search_space, max_no_impr, step_size):
    count = 0

    while count < max_no_impr:
        candidate = {}
        candidate['vector'] = take_step(
            search_space, best['vector'], step_size)
        candidate['cost'] = objective_function(candidate['vector'])
        if candidate['cost'] < best['cost']:
            best = candidate
            count = 0
        else:
            count += 1

    return best


def construct_initial_set(search_space, set_size, max_no_impr, step_size):
    diverse_set = []

    while len(diverse_set) < set_size:
        candidate = {}
        candidate['vector'] = generate_random_vector(search_space)
        candidate['cost'] = objective_function(candidate['vector'])
        candidate = local_search(
            candidate, search_space, max_no_impr, step_size)
        if not any([candidate['vector'] == representative['vector'] for representative in diverse_set]):
            diverse_set.append(candidate)

    return diverse_set


def calculate_euclidean_distance(from_point, to_point):
    return sqrt(sum((from_point[i] - to_point[i])**2 for i in range(len(from_point))))


def calculate_distance_from_set(observed_element, set):
    return sum(calculate_euclidean_distance(observed_element, el['vector']) for el in set)


def diversify(diverse_set, elite_num, ref_set_size):
    sorted(diverse_set, key=lambda x: x['cost'])

    ref_set = []
    remainders = []

    for i, representative in enumerate(diverse_set):
        if i <= elite_num:
            ref_set.append(representative)
        else:
            remainders.append(representative)

    for remainder in remainders:
        remainder['distance'] = calculate_distance_from_set(
            remainder['vector'], ref_set)

    sorted(remainders, key=lambda x: x['distance'])

    for remainder in remainders:
        if len(ref_set) >= ref_set_size:
            break
        ref_set.append(remainder)

    return ref_set, ref_set[0]


def select_sub_sets(ref_set):
    new_top_individuals = []
    remainders = []
    for representative in ref_set:
        if representative.get('new'):
            new_top_individuals.append(representative)
        else:
            remainders.append(representative)

    if len(remainders) == 0:
        remainders = new_top_individuals

    sub_sets = []

    for addition in new_top_individuals:
        for remainder in remainders:
            if addition != remainder and [remainder, addition] not in sub_sets:
                sub_sets.append([addition, remainder])

    return sub_sets


def recombine(pair, search_space):
    childeren = []

    first_element, secound_element = pair
    distance = random_within_bounds(0, calculate_euclidean_distance(
        first_element['vector'], secound_element['vector']))

    for parent in pair:
        step = +distance if random.random() < 0.5 else -distance
        new_child = {}
        new_child['vector'] = [0] * len(search_space)
        for i in range(len(new_child['vector'])):
            new_child['vector'][i] = parent['vector'][i] + step
            if new_child['vector'][i] < search_space[i][0]:
                new_child['vector'][i] = search_space[i][0]
            elif new_child['vector'][i] > search_space[i][1]:
                new_child['vector'][i] = search_space[i][1]
        new_child['cost'] = objective_function(new_child['vector'])
        if not any([new_child['vector'] == selected_child['vector'] for selected_child in childeren]):
            childeren.append(new_child)

    return childeren


def explore_sub_sets(search_space, ref_set, max_no_impr, step_size):
    was_changed = False
    sub_sets = select_sub_sets(ref_set)
    for representative in ref_set:
        representative['new'] = False

    for pair in sub_sets:
        candidates = recombine(pair, search_space)
        improved = []
        for candidate in candidates:
            improved.append(local_search(
                candidate, search_space, max_no_impr, step_size))

        for el in improved:
            if not any([el['vector'] == representative['vector'] for representative in ref_set]):
                el['new'] = True
                sorted(ref_set, key=lambda x: x['cost'])
                if el['cost'] < ref_set[-1]['cost']:
                    ref_set.pop()
                    ref_set.append(el)
                    was_changed = True

    return was_changed


def scatter_search(search_space, max_iter, ref_set_size, div_set_size, max_no_impr, step_size, max_elite):
    diverse_set = construct_initial_set(
        search_space, div_set_size, max_no_impr, step_size)

    ref_set, best = diversify(diverse_set, max_elite, ref_set_size)

    for el in ref_set:
        el['new'] = True

    for _ in range(max_iter):
        was_changed = explore_sub_sets(
            search_space, ref_set, max_no_impr, step_size)
        sorted(ref_set, key=lambda x: x['cost'])
        if ref_set[0]['cost'] < best['cost']:
            best = ref_set[0]

        if not was_changed:
            break

    return best


if __name__ == '__main__':

    # f = sum(xi**2), i = {1,2...n}, -5 <= xi <= 5

    problem_size = 3
    search_space = [[-5, 5] for _ in range(problem_size)]
    max_iter = 100
    step_size = (search_space[0][1]-search_space[0][0])*0.005
    max_no_impr = 30
    ref_set_size = 20
    diverse_set_size = 50
    elite_num = 10

    best = scatter_search(search_space, max_iter, ref_set_size,
                          diverse_set_size, max_no_impr, step_size, elite_num)
    print(f"Done. Best Solution: c={best['cost']}, v={best['vector']}")
